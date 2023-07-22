import {User} from '../../../../6_entities/user';

export interface AuthState {
  authorized: boolean | undefined,
  currentUser: User | null
}
