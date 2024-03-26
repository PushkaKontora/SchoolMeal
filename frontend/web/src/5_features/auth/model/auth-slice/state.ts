import {User} from '../../../../6_entities/user';
import {JwtPayload} from '../jwt-payload.ts';
import {Role} from '../role.ts';

export interface AuthState {
  authorized: boolean | undefined,
  currentUser: User | null,
  userRole: Role | undefined,
  jwtPayload: JwtPayload | null,
  needRoleChecking: boolean,
  needTokenRefresh: boolean
}
