import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { EmailService } from "src/email/email.service";
import { AuthController } from "./auth.controller";
import { AuthCryptoService } from "./auth.crypto";
import { AuthService } from "./auth.service";
import { AuthRefreshStrategy, AuthStrategy } from "./auth.strategy";


@Module({
  imports: [JwtModule.register({})],
  controllers: [AuthController],
  providers: [
    AuthService,
    AuthCryptoService,
    AuthStrategy,
    AuthRefreshStrategy,
    EmailService
  ]
})
export class AuthModule { }