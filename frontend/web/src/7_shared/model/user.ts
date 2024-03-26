import {Role} from './role.ts';

/**
 * @deprecated
 */
export type User = {
  id: string,
  login: string,
  lastName: string,
  firstName: string,
  role: Role,
  phone: string,
  email: string
}
