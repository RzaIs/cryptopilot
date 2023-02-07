import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
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
    AuthRefreshStrategy
  ]
})
export class AuthModule { }