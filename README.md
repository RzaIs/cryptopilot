
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
  "key" "MIIBCgKCAQEAqryK4Acc40xhK/cJ+sjf"
}
```
<br/>

### POST `/auth/login`
Request Body
```json
{
  "username": "rzais",
  "email": "rza@email.com",
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

### POST `/auth/register`
Request Body
```json
{
  "username": "rzais",
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
