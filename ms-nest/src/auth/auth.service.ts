import { BadRequestException, ForbiddenException, Injectable, NotFoundException, UnauthorizedException } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { JwtService } from "@nestjs/jwt";
import { OneTimePassword, OneTimeResetToken, PrivateKey, User } from "@prisma/client";
import { hash, verify } from "argon2";
import { randomUUID } from "crypto";
import { EmailService } from "src/email/email.service";
import { none, Optional } from "src/helper/optional";
import { PrismaService } from "src/prisma/prisma.service";
import { UserResponseModel } from "src/user/user.models";
import { AuthCryptoService } from "./auth.crypto";
import { AuthResponseModel, CreateOTPResponseModel, LoginRequestModel, PublicKeyResponseModel, RegisterRequestModel, ResetPasswordRequestModel, ResetTokenResponseModel, TokensReponseModel, ValidateOTPRequestModel } from "./auth.models";


@Injectable()
export class AuthService {
  constructor(
    private readonly crypto: AuthCryptoService,
    private readonly prisma: PrismaService,
    private readonly config: ConfigService,
    private readonly email: EmailService,
    private readonly jwt: JwtService,
  ) { }


  async login(credentials: LoginRequestModel): Promise<AuthResponseModel> {

    const [user, keyData] = await Promise.all([
      this.prisma.user.findUnique({
        where: { username: credentials.username }
      }),
      this.prisma.privateKey.findUnique({
        where: { id: credentials.keyID }
      })
    ])

    if (none(user) || none(keyData)) {
      throw new ForbiddenException('Incorrect credentials')
    }

    if (keyData.created < this.getDateWithDeadline(2)) {
      throw new ForbiddenException('Encryption key is expired')
    }

    const password = this.crypto.decrypt(
      credentials.encryptedPassword,
      keyData.privateKey
    )

    const verified = await verify(user.secret, password)

    if (!verified) {
      throw new ForbiddenException('Incorrect credentials')
    }

    const [accessToken, refreshToken] = await Promise.all([
      this.generateAccessToken(user.id, user.email),
      this.generateRefreshToken(user.id, user.email)
    ])

    return {
      user: new UserResponseModel(user),
      tokens: { accessToken, refreshToken }
    }
  }

  async register(credentials: RegisterRequestModel): Promise<AuthResponseModel> {
    const keyData: Optional<PrivateKey> = await this.prisma.privateKey.findUnique({
      where: { id: credentials.keyID }
    })

    if (none(keyData)) {
      throw new ForbiddenException('Session timeout')
    }

    if (keyData.created < this.getDateWithDeadline(2)) {
      throw new ForbiddenException('Encryption key is expired')
    }

    const password = this.crypto.decrypt(
      credentials.encryptedPassword,
      keyData.privateKey
    )

    const secretHash = await hash(password)

    try {
      const user = await this.prisma.user.create({
        data: {
          email: credentials.email,
          username: credentials.username,
          secret: secretHash
        }
      })

      const [accessToken, refreshToken] = await Promise.all([
        this.generateAccessToken(user.id, user.email),
        this.generateRefreshToken(user.id, user.email)
      ])

      return {
        user: new UserResponseModel(user),
        tokens: { accessToken, refreshToken }
      }

    } catch (error) {
      if (error.code === 'P2002') {
        throw new ForbiddenException('Credentials are already taken!')
      } else {
        throw error
      }
    }
  }
  
  async sendResetPasswordOTP(email: string): Promise<CreateOTPResponseModel> {

    const user: Optional<User> = await this.prisma.user.findUnique({
      where: { email }
    })

    if (none(user)) {
      throw new NotFoundException('User with the provided email not found')
    }

    const otp = await this.prisma.oneTimePassword.create({
      data: {
        challenge: randomUUID(),
        password: Math.floor(100000 + Math.random() * 900000).toString(),
        userId: user.id
      }
    })

    this.email.sendEmail({
      receiver: user.email,
      subject: `Password reset requested for account ${user.username}`,
      html: `\
        <h1>Here is your one time password</h1><br/> \
        <h2>${otp.password}</h2><br/> \
        <h3>If you did not requested it, you can safely ignore this email.</h3>`
    })

    return { challage: otp.challenge }
  }

  async validateOTP(challenge: string, password: string): Promise<ResetTokenResponseModel> {
    const otp: Optional<OneTimePassword> = await this.prisma.oneTimePassword.findUnique({
      where: { challenge }
    })

    if (none(otp)) {
      throw new NotFoundException('Invalid or expired OTP challage')
    }

    if (otp.created < this.getDateWithDeadline(10)) {
      throw new ForbiddenException('One-time-password is expired')
    }

    if (otp.password !== password) {
      throw new UnauthorizedException('Invalid one-time-password')
    }

    const [resetToken, _] = await Promise.all([
      this.prisma.oneTimeResetToken.create({
        data: {
          uuid: randomUUID() + randomUUID(),
          userId: otp.userId
        }
      }),
      this.prisma.oneTimePassword.delete({
        where: { challenge }
      })
    ])

    return { uuid: resetToken.uuid }
  }

  async resetPassword(params: ResetPasswordRequestModel) {
    const token: Optional<OneTimeResetToken> = await this.prisma
      .oneTimeResetToken
      .findUnique({
        where: { 
          uuid: params.oneTimeToken 
        }
      })

    if (none(token)) {
      throw new UnauthorizedException('Invalid password-reset-token')
    }

    if (token.created < this.getDateWithDeadline(10)) {
      throw new ForbiddenException('One-time-reset-token is expired')
    }

    const keyData: Optional<PrivateKey> = await this.prisma.privateKey.findUnique({
      where: { id: params.keyID }
    })

    if (none(keyData)) {
      throw new NotFoundException('Encryption key with the given id not found')
    }

    if (keyData.created < this.getDateWithDeadline(2)) {
      throw new ForbiddenException('Encryption key is expired')
    }

    const newPassword = this.crypto.decrypt(
      params.encryptedPassword,
      keyData.privateKey
    )

    const secretHash = await hash(newPassword)

    const [user, _] = await Promise.all([
      this.prisma.user.update({
        where: {
          id: token.userId
        },
        data: {
          secret: secretHash
        }
      }),
      this.prisma.oneTimeResetToken.delete({
        where: {
          uuid: token.uuid
        }
      })
    ])

    if (none(user)) {
      throw new NotFoundException('User matching with the given token not found')
    }

    const [accessToken, refreshToken] = await Promise.all([
      this.generateAccessToken(user.id, user.email),
      this.generateRefreshToken(user.id, user.email)
    ])

    return {
      user: new UserResponseModel(user),
      tokens: { accessToken, refreshToken }
    }
  }

  async generateAccessToken(userID: number, email: string): Promise<string> {
    const token = await this.jwt.signAsync({
      sub: userID,
      email: email
    },
      {
        expiresIn: '72h',
        secret: this.config.get('JWT_ACCESS_SECRET')
      }
    )
    return token
  }

  async generateRefreshToken(userID: number, email: string): Promise<string> {
    const token = await this.jwt.signAsync(
      {
        sub: userID,
        email: email
      },
      {
        expiresIn: '72 days',
        secret: this.config.get('JWT_REFRESH_SECRET')
      }
    )
    return token
  }

  async refreshTokens(userID: number, email: string): Promise<TokensReponseModel> {
    const [accessToken, refreshToken] = await Promise.all([
      this.generateAccessToken(userID, email),
      this.generateRefreshToken(userID, email)
    ])
    return { accessToken, refreshToken }
  }

  async generateKeys(): Promise<PublicKeyResponseModel> {
    const { publicKey, privateKey } = this.crypto.generateKeys()

    const privateKeyData = await this.prisma.privateKey.create({
      data: { privateKey }
    })

    return { id: privateKeyData.id, key: publicKey }
  }

  async clearOldKeys(): Promise<void> {
    await this.prisma.privateKey.deleteMany({
      where: {
        created: {
          lte: this.getDateWithDeadline(2)
        }
      }
    })
  }

  async cleanOldOTPs(): Promise<void> {
    await this.prisma.oneTimePassword.deleteMany({
      where: {
        created: {
          lte: this.getDateWithDeadline(10)
        }
      }
    })
  }

  async cleanOldOTRTs(): Promise<void> {
    await this.prisma.oneTimeResetToken.deleteMany({
      where: {
        created: {
          lte: this.getDateWithDeadline(10)
        }
      }
    })
  }

  private getDateWithDeadline(minutes: number): Date {
    const date = new Date()
    date.setMinutes(date.getMinutes() - minutes)
    return date
  }

  // Unsafe Login - Development Only

  async unsafeLogin(credentials: {
    username: string,
    password: string,
  }): Promise<AuthResponseModel> {
    const user: Optional<User> = await this.prisma.user.findUnique({
      where: {
        username: credentials.username
      }
    })

    if (none(user)) {
      throw new ForbiddenException('Incorrect credentials')
    }

    const verified = await verify(user.secret, credentials.password)

    if (!verified) {
      throw new ForbiddenException('Incorrect credentials')
    }

    const [accessToken, refreshToken] = await Promise.all([
      this.generateAccessToken(user.id, user.email),
      this.generateRefreshToken(user.id, user.email)
    ])

    return {
      user: new UserResponseModel(user),
      tokens: { accessToken, refreshToken }
    }
  }

  // Unsafe Register - Development Only

  async unsafeRegister(credentials: {
    email: string
    username: string,
    password: string,
  }): Promise<AuthResponseModel> {

    const secretHash = await hash(credentials.password)

    try {
      const user = await this.prisma.user.create({
        data: {
          email: credentials.email,
          username: credentials.username,
          secret: secretHash
        }
      })

      const [accessToken, refreshToken] = await Promise.all([
        this.generateAccessToken(user.id, user.email),
        this.generateRefreshToken(user.id, user.email)
      ])

      return {
        user: new UserResponseModel(user),
        tokens: { accessToken, refreshToken }
      }

    } catch (error) {
      if (error.code === 'P2002') {
        throw new ForbiddenException('Credentials are already taken!')
      } else {
        throw error
      }
    }
  }
}