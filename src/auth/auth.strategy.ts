import { Injectable } from '@nestjs/common'
import { ConfigService } from '@nestjs/config'
import { AuthGuard, PassportStrategy } from '@nestjs/passport'
import { User } from '@prisma/client'
import { ExtractJwt, Strategy } from 'passport-jwt'
import { Optional } from 'src/helper/optional'
import { PrismaService } from 'src/prisma/prisma.service'


@Injectable()
export class AuthStrategy extends PassportStrategy(Strategy, 'jwt') {
  
  public static JwtGuard = AuthGuard('jwt')

  constructor(
    private readonly prisma: PrismaService,
    config: ConfigService
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromHeader('access-token'),
      secretOrKey: config.get('JWT_ACCESS_SECRET')
    })
  }

  async validate(payload: { sub: number }): Promise<Optional<User>> {
    return await this.prisma.user.findUnique({
      where: {
        id: payload.sub
      }
    })
  }
}

@Injectable()
export class AuthRefreshStrategy extends PassportStrategy(Strategy, 'jwt-refresh') {
  public static JwtGuard = AuthGuard('jwt-refresh')

  constructor(
    private readonly prisma: PrismaService,
    config: ConfigService
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromHeader('refresh-token'),
      secretOrKey: config.get('JWT_REFRESH_SECRET')
    })
  }

  async validate(payload: { sub: number }): Promise<Optional<User>> {
    return await this.prisma.user.findUnique({
      where: {
        id: payload.sub
      }
    })
  }
}