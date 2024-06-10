import {ROLE_DEFAULT_ROUTES} from './config.ts';
import {Role} from '../../../7_shared/lib/auth';

export function chooseRedirectRoute(role: Role) {
  return ROLE_DEFAULT_ROUTES[role];
}
