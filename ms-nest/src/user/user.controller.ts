import { Controller, Get, Response, UnauthorizedException, UseGuards } from "@nestjs/common";
import { User } from "@prisma/client";
import axios, { AxiosError } from "axios";
import { GetUser } from "src/auth/auth.decorators";
import { AuthStrategy } from "src/auth/auth.strategy";
import { msaxios } from "src/helper/ms.axios";
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

  @Get('example')
  async getExample(): Promise<any> {
    return (await msaxios(() => axios.get('http://ms-data:4040/example/data'))).data
  }
}