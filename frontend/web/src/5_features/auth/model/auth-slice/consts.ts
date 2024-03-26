import {AuthState} from './state';

export const initialState: AuthState = {
  authorized: undefined,
  currentUser: null,
  jwtPayload: null,
  userRole: undefined,
  needRoleChecking: false,
  needTokenRefresh: false
};
