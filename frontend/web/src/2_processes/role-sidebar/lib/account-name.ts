import {User} from '../../../7_shared/model/user.ts';

export function getAccountName(user?: User) {
  return [user?.firstName, user?.lastName].join(' ');
}
