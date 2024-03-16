import {Role} from '../../../7_shared/model/role.ts';
import {ROLE_DEFAULT_ROUTES} from './config.ts';

export function chooseRedirectRoute(role: Role) {
  return ROLE_DEFAULT_ROUTES[role];
}
