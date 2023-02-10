import { ForbiddenException, Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { JwtService } from "@nestjs/jwt";
import { PrivateKey } from "@prisma/client";
import { hash, verify } from "argon2";
import { none, Optional } from "src/helper/optional";
import { PrismaService } from "src/prisma/prisma.service";
import { UserResponseModel } from "src/user/user.models";
import { AuthCryptoService } from "./auth.crypto";
import { AuthResponseModel, LoginRequestModel, PublicKeyResponseModel, RegisterRequestModel, TokensReponseModel } from "./auth.models";


@Injectable()
export class AuthService {
  constructor(
    private readonly crypto: AuthCryptoService,
    private readonly prisma: PrismaService,
    private readonly config: ConfigService,
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

    const password = await this.crypto.decrypt(
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