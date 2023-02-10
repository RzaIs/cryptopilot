import { Injectable, NotFoundException } from "@nestjs/common";
import { User } from "@prisma/client";
import { Optional, some } from "src/helper/optional";
import { PrismaService } from "src/prisma/prisma.service";
import { UserResponseModel } from "./user.models";


@Injectable()
export class UserService {
  constructor(private readonly prisma: PrismaService) { }

  async getUserById(id: number): Promise<UserResponseModel> {
    const user: Optional<User> = await this.prisma.user.findUnique({
      where: { id }
    })

    if (some(user)) {
      return new UserResponseModel(user)
    } else {
      throw new NotFoundException('User with specified id does not exist!')
    }
  }
}