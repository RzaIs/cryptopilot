import { ForbiddenException, Injectable, NotFoundException, UnauthorizedException } from "@nestjs/common";
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
      subject: 'Password reset requested',
      html: `<h1>${otp.password}</h1>`
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
    const token: Optional<OneTimeResetToken & { user: User }> = await this.prisma
      .oneTimeResetToken
      .findUnique({
        where: { uuid: params.oneTimeToken },
        include: {
          user: true
        }
      })

    console.log(token)

    if (none(token)) {
      throw new UnauthorizedException('Invalid password-reset-token')
    }

    const keyData: Optional<PrivateKey> = await this.prisma.privateKey.findUnique({
      where: { id: params.keyID }
    })

    console.log(keyData)


    if (none(keyData)) {
      throw new NotFoundException('Encryption key with the given id not found')
    }

    const newPassword = this.crypto.decrypt(
      params.encryptedPassword,
      keyData.privateKey
    )

    console.log(newPassword)

    const secretHash = await hash(newPassword)

    console.log(secretHash)

    const user: Optional<User> = await this.prisma.user.update({
      where: {
        id: token.userId
      },
      data: {
        secret: secretHash
      }
    })

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

    setTimeout(() => {
      this.clearOldKeys().then(() => {
        console.log('✅ Old Keys Have Been Successfully Removed ✅')
      }).catch((error) => {
        console.log('⛔️ An Error Occured While Clearing Old Keys ⛔️')
      })
    }, 0.0);

    return { id: privateKeyData.id, key: publicKey }
  }

  async clearOldKeys(): Promise<void> {
    const date = new Date()
    date.setSeconds(date.getSeconds() - 60)
    await this.prisma.privateKey.deleteMany({
      where: {
        created: {
          lte: new Date(date)
        }
      }
    })
  }
}