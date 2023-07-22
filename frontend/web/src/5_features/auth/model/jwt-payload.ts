import {Role} from '../../../7_shared/model/role';

export type JwtPayload = {
  type: string,
  user_id: number,
  role: Role,
  expires_in: number
}
