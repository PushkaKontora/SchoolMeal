import {Role} from '../../../7_shared/model/role';

export type User = {
  id: number,
  lastName: string,
  firstName: string,
  login: string,
  role: Role,
  phone: string,
  email: string,
  photoPath: string,
  createdAt: Date
}
