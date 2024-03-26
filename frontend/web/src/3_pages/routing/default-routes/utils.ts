import {ROLE_DEFAULT_ROUTES} from './config.ts';
import {Role} from '../../../5_features/auth';

export function chooseRedirectRoute(role: Role) {
  return ROLE_DEFAULT_ROUTES[role];
}
