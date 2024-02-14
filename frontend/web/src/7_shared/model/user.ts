import {Role} from './role.ts';

export type User = {
  id: string,
  login: string,
  lastName: string,
  firstName: string,
  role: Role,
  phone: string,
  email: string
}
