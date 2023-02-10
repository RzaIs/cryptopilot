import { Body, Controller, Get, HttpCode, HttpStatus, Post, UseGuards } from "@nestjs/common";
import { User } from "@prisma/client";
import { GetUser } from "./auth.decorators";
import { AuthResponseModel, LoginRequestModel, PublicKeyResponseModel, RegisterRequestModel, TokensReponseModel } from "./auth.models";
import { AuthService } from "./auth.service";
import { AuthRefreshStrategy } from "./auth.strategy";


@Controller('auth')
export class AuthController {
  constructor(private readonly service: AuthService) { }

  @Get('key')
  async getPublicKey(): Promise<PublicKeyResponseModel> {
    return this.service.generateKeys()
  }

  @HttpCode(HttpStatus.OK)
  @Post('login')
  async login(@Body() credentials: LoginRequestModel): Promise<AuthResponseModel> {
    return this.service.login(credentials)
  }

  @Post('register')
  async register(@Body() credentials: RegisterRequestModel): Promise<AuthResponseModel> {
    return this.service.register(credentials)
  }

  @UseGuards(AuthRefreshStrategy.JwtGuard)
  @Get('refresh-token')
  async refreshToken(@GetUser() user: User) {
    return this.service.refreshTokens(user.id, user.email)
  }
}