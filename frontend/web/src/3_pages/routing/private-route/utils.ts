import {RoleOrAny} from './types.ts';
import {User} from '../../../7_shared/model/user.ts';

export function isRoleMatching(requiredRole: RoleOrAny, user: User | undefined) {
  return requiredRole === user?.role ||
    (requiredRole === 'any' && user);
}