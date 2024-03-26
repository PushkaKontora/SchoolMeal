export type JwtPayload = {
  jti: string,
  user_id: string,
  role: 1 | 2,
  iat: number,
  exp: number,
  last_name: string,
  first_name: string,
  patronymic: string
}
