import {UUID} from '../../../7_shared/model/uuid';

export type JwtPayload = {
  jti: UUID,
  token: string,
  user_id: UUID,
  device_id: UUID,
  iat: number,
  exp: number
}
