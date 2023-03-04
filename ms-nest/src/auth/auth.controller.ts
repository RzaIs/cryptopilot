import { Body, Controller, Get, HttpCode, HttpStatus, Param, Post, UseGuards } from "@nestjs/common";
import { User } from "@prisma/client";
import { GetUser } from "./auth.decorators";
import { AuthResponseModel, CreateOTPResponseModel, LoginRequestModel, PublicKeyResponseModel, RegisterRequestModel, ForgetPasswordRequestModel, ResetTokenResponseModel, TokensReponseModel, ValidateOTPRequestModel, ResetPasswordRequestModel } from "./auth.models";
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

  @Post('forget-password')
  async forgetPassword(@Body() body: ForgetPasswordRequestModel): Promise<CreateOTPResponseModel> {
    return this.service.sendResetPasswordOTP(body.email)
  }

  @Post('validate-otp/:challage')
  async validateOTP(
    @Param('challage') challage: string,
    @Body() body: ValidateOTPRequestModel
  ): Promise<ResetTokenResponseModel> {
    return this.service.validateOTP(challage, body.oneTimePassword)
  }

  @Post('reset-password')
  async resetPassword(@Body() body: ResetPasswordRequestModel) {
    return this.service.resetPassword(body)
  }

  @UseGuards(AuthRefreshStrategy.JwtGuard)
  @Get('refresh-token')
  async refreshToken(@GetUser() user: User) {
    return this.service.refreshTokens(user.id, user.email)
  }
}