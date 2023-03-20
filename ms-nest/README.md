
# ENDPOINTS

<br/>

## AUTH

<br/>

### GET `/auth/key`

Request Body
```json
null
```
Response Body
```json
{
  "id": 24533,
  "key": "MIIBCgKCAQEAqryK4Acc40xhK/cJ+sjf"
}
```
<br/>

### POST `/auth/register`
Request Body
```json
{
  "username": "your_username",
  "email": "email@example.com",
  "encryptedPassword": "oAQcgupQhBOOuOziRtuYhEyYYNY0ezDKh",
  "keyID": 248
}
```
Response Body
```json
{
  "user": {
    "id": 124,
    "email": "email@example.com",
    "username": "your_username",
    "created": "2023-02-07T21:02:35.294Z",
    "updated": "2023-02-07T21:02:35.294Z"
  },
  "tokens": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp"
  }
}
```

### POST `/auth/login`
Request Body
```json
{
  "username": "your_username",
  "encryptedPassword": "oAQcgupQhBOOuOziRtuYhEyYYNY0ezDKh",
  "keyID": 832
}
```
Response Body
```json
{
  "user": {
    "id": 124,
    "email": "email@example.com",
    "username": "your_username",
    "created": "2023-02-07T21:02:35.294Z",
    "updated": "2023-02-07T21:02:35.294Z"
  },
  "tokens": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp"
  }
}
```
<br/>

### POST `/auth/forget-password`
Request Body
```json
{
  "email": "email@example.com"
}
```
Response Body
```json
{
  "challage": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp"
}
```
<br/>

### POST `/auth/validate-otp/{challage}`
Request Body
```json
{
  "oneTimePassword": "123456"
}
```
Response Body
```json
{
  "uuid": "oAQcgupQhBOOuOziRtuYhEyYYNY0ezDKh"
}
```

<br/>

### POST `/auth/reset-password`
Request Body
```json
{
  "oneTimeToken": "oAQcgupQhBOOuOziRtuYhEyYYNY0ezDKh",
  "encryptedPassword": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp",
  "keyID": 324
}
```
Response Body
```json
null
```

<br/>

### GET `/auth/refresh-token`
Request Body
```json
null
```
Response Body
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp"
}
```

<br/>

## USER

<br/>

### GET `/user/me`
Request Body
```json
null
```
```json
{
  "id": 124,
  "email": "email@example.com",
  "username": "your_username",
  "created": "2023-02-07T21:02:35.294Z",
  "updated": "2023-02-07T21:02:35.294Z"
}
```

<br/>
<br/>

# Auth Checks

## for regular auth check you have to have your `access-token` in your request header.

<br/>

## for refreshing expired `access-token` you have to have your `refresh-token` in your header

<br/>
<br/>

# Addition Info Abount Encryption

## you can encrypt your password with the key you obtained from `/auth/key` with the help of lib `jsencrypt` . code example:
<br/>

```ts
import JSEncrypt from "jsencrypt"

const encryptor = new JSEncrypt()

function encrypt(password: string, key: string): string | null {
  encryptor.setPublicKey(key)

  const encryptedPassword = this.encryptor.encrypt(password)
  
  if (encryptedPassword === false) {
    return null
  } else {
    return encryptedPassword
  }
}

```

<br/>
<br/>

# Addition Info Password Reset

### In order to reset password you first make a request to `/auth/forget-password` then you will get a string `challage` and will receive a 6 digit one time password in the email of the user. then you will send this `oneTimePassword` to `/auth/validate-otp/{challage}` with `challage` you received earlier. if they match and are correct you will get a `uuid` which is token for resetting your password. then you will request to reset your password via `/auth/reset-password`. Note: you have to encrypt the new password like you did in login and register and will send encrypted password and keyID alongside your `oneTimeToken` a.k.a `uuid`.

