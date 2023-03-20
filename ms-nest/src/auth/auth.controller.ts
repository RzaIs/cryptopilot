import { Body, Controller, Get, HttpCode, HttpStatus, Param, Post, UseGuards } from "@nestjs/common";
import { User } from "@prisma/client";
import { executeAsync, execute } from "src/helper/service.executer";
import { GetUser } from "./auth.decorators";
import { AuthResponseModel, CreateOTPResponseModel, LoginRequestModel, PublicKeyResponseModel, RegisterRequestModel, ForgetPasswordRequestModel, ResetTokenResponseModel, TokensReponseModel, ValidateOTPRequestModel, ResetPasswordRequestModel } from "./auth.models";
import { AuthService } from "./auth.service";
import { AuthRefreshStrategy } from "./auth.strategy";


@Controller('auth')
export class AuthController {
  constructor(private readonly service: AuthService) { }

  @Get('key')
  async getPublicKey(): Promise<PublicKeyResponseModel> {
    return executeAsync(this.service.generateKeys())
  }

  @HttpCode(HttpStatus.OK)
  @Post('login')
  async login(@Body() credentials: LoginRequestModel): Promise<AuthResponseModel> {
    return executeAsync(this.service.login(credentials))
  }

  @Post('register')
  async register(@Body() credentials: RegisterRequestModel): Promise<AuthResponseModel> {
    return executeAsync(this.service.register(credentials))
  }

  @Post('forget-password')
  async forgetPassword(@Body() body: ForgetPasswordRequestModel): Promise<CreateOTPResponseModel> {
    return executeAsync(this.service.sendResetPasswordOTP(body.email))
  }

  @Post('validate-otp/:challage')
  async validateOTP(
    @Param('challage') challage: string,
    @Body() body: ValidateOTPRequestModel
  ): Promise<ResetTokenResponseModel> {
    return executeAsync(this.service.validateOTP(challage, body.oneTimePassword))
  }

  @Post('reset-password')
  async resetPassword(@Body() body: ResetPasswordRequestModel): Promise<AuthResponseModel> {
    return executeAsync(this.service.resetPassword(body))
  }

  @UseGuards(AuthRefreshStrategy.JwtGuard)
  @Get('refresh-token')
  async refreshToken(@GetUser() user: User): Promise<TokensReponseModel> {
    return executeAsync(this.service.refreshTokens(user.id, user.email))
  }

  @Get('clean-up')
  async cleanUpDB(): Promise<void> {
    try {
      await this.service.clearOldKeys()
      await this.service.cleanOldOTPs()
      await this.service.cleanOldOTRTs()
      console.log('✅ Old keys, OTPs and OTRTs have been successfully removed ✅')
    } catch (error) {
      console.log(`⛔️ An error occured while clean up ⛔️\nERROR: ${error}`)
    }
  }
}