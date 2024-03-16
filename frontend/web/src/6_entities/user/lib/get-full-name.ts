import {User} from '../../../7_shared/model/user.ts';

export function getFullName(user?: User) {
  return `${user?.firstName ?? ''} ${user?.lastName ?? ''}`;
}
