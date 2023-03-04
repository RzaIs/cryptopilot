import { IsEmail, IsNotEmpty } from "class-validator"
import { UserResponseModel } from "src/user/user.models"

// Request Models

export class LoginRequestModel {
  @IsNotEmpty() username: string
  @IsNotEmpty() encryptedPassword: string
  @IsNotEmpty() keyID: number
}

export class RegisterRequestModel {
  @IsEmail()
  @IsNotEmpty() email: string
  @IsNotEmpty() username: string
  @IsNotEmpty() encryptedPassword: string
  @IsNotEmpty() keyID: number
}

export class ForgetPasswordRequestModel {
  @IsEmail()
  @IsNotEmpty()
  email: string
}

export class ValidateOTPRequestModel {
  @IsNotEmpty()
  oneTimePassword: string
}

export class ResetPasswordRequestModel {
  @IsNotEmpty() oneTimeToken: string
  @IsNotEmpty() encryptedPassword: string
  @IsNotEmpty() keyID: number
}

// Response Models

export interface PublicKeyResponseModel {
  id: number,
  key: string
}

export interface TokensReponseModel {
  accessToken: string,
  refreshToken: string
}

export interface AuthResponseModel {
  user: UserResponseModel,
  tokens: TokensReponseModel
}

export interface CreateOTPResponseModel {
  challage: string
}

export interface ResetTokenResponseModel {
  uuid: string
}