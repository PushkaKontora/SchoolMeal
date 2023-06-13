import {RoleOrAny} from './types';
import {User} from '../../6_entities/user';

export function isRoleMatching(requiredRole: RoleOrAny, user: User | undefined | null) {
  return requiredRole === user?.role ||
    (requiredRole === 'any' && user);
}
