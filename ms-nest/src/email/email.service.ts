import { Injectable, NotFoundException } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { some, Optional } from "src/helper/optional";
import { createTransport, Transporter } from 'nodemailer';

@Injectable()
export class EmailService {

  private readonly sender: string
  private readonly transporter: Transporter

  constructor(
    private readonly config: ConfigService,
  ) {
    const user: Optional<string> = this.config.get('EMAIL_ADDRESS')
    const pass: Optional<string> = this.config.get('EMAIL_PASSWORD')
    if (some(user) && some(pass)) {
      this.sender = user
      this.transporter = createTransport({
        service: 'gmail',
        auth: { user, pass }
      })
    } else {
      throw new NotFoundException('"EMAIL CRED" is missing ⛔️')
    }
  }

  async sendEmail(params: {
    receiver: string,
    subject: string,
    html: string,
  }): Promise<void> {

    const mailOpt = {
      from: {
        name: 'Cryptopilot',
        address: this.sender
      },
      to: params.receiver,
      subject: params.subject,
      html:  params.html,
    }

    return new Promise((resolve, reject) => {
      this.transporter.sendMail(mailOpt, (error, info) => {
        if (error) {
          reject(error)
        } else {
          resolve()
          console.log('email sent:', {
            to: params.receiver,
            title: params.subject,
            date: Date()
          });
        }
      })
    })
  }
}