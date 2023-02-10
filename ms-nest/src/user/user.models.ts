import { User } from "@prisma/client";

// Response Models

export class UserResponseModel {
  readonly id: number
  readonly email: string
  readonly username: string
  readonly created: Date
  readonly updated: Date

  constructor(user: User) {
    this.id = user.id
    this.email = user.email
    this.username = user.username
    this.created = user.created
    this.updated = user.updated
  }
}
