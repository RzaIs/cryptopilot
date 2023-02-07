import { Controller, Get, UseGuards } from "@nestjs/common";
import { User } from "@prisma/client";
import { GetUser } from "src/auth/auth.decorators";
import { AuthStrategy } from "src/auth/auth.strategy";
import { UserResponseModel } from "./user.models";
import { UserService } from "./user.service";


@UseGuards(AuthStrategy.JwtGuard)
@Controller('user')
export class UserController {
  constructor(private readonly service: UserService) { }

  @Get('me')
  async getSelfUser(@GetUser() user: User): Promise<UserResponseModel> {
    return new UserResponseModel(user)
  }
}