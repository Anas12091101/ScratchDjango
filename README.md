# Django Scratch

A SaaS based django application built from scratch.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Anas12091101/ScratchDjango
```

Go to the project directory

```bash
  cd ScratchDjango
```

Add .env file

```bash
  touch .env
  // Following variables should be set in environment
    DJANGO_SECRET_KEY
    DATABASE_URL
    EMAIL_HOST_PASSWORD
    EMAIL_HOST_USER
    PAYPAL_CLIENT_ID
    PAYPAL_CLIENT_SECRET
```

### Running with docker

```bash
  docker compose up
  docker exec -it <web container name> -bash
  python manage.py migrate
```

### Running without docker

```bash
  pip install -r req/local.txt
  python manage.py migrate
  python manage.py runserver
```

## API Reference

#### Register User

Registers the user

```http
  POST /user/register_user/
```

| Parameter     | Type     | Description                                                                         |
| :------------ | :------- | :---------------------------------------------------------------------------------- |
| `name`        | `string` | **Required** Your name                                                              |
| `otp_enabled` | `string` | **Required** None or "GA"(for google Authenticator) or "Email"(for email based OTP) |
| `email`       | `string` | **Required** Your valid email                                                       |
| `password`    | `string` | **Required** Password                                                               |

#### Login

Returns JWT token on valid credentials if OTP is not enabled else the type of OTP

```http
  POST /user/login/
```

| Parameter  | Type     | Description  |
| :--------- | :------- | :----------- |
| `email`    | `string` | **Required** |
| `password` | `string` | **Required** |

#### Check OTP

Returns JWT token on valid credentials and OTP

```http
  POST /user/check_otp/
```

| Parameter  | Type     | Description  |
| :--------- | :------- | :----------- |
| `email`    | `string` | **Required** |
| `password` | `string` | **Required** |
| `otp`      | `string` | **Required** |

#### Password Reset

Sends email with the reset token

```http
  POST /user/api/password_reset/
```

| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `email`   | `string` | **Required** |

#### Password Confirm Reset

Resets the password

```http
  POST /user/api/password_reset/confirm/
```

| Parameter  | Type     | Description  |
| :--------- | :------- | :----------- |
| `token`    | `string` | **Required** |
| `password` | `string` | **Required** |
