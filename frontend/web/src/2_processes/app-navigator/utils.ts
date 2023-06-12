import {Role} from '../../7_shared/model/role';
import {ROLE_DEFAULT_ROUTES} from './config';

export function chooseRedirectRoute(role: Role) {
  return ROLE_DEFAULT_ROUTES[role];
}
