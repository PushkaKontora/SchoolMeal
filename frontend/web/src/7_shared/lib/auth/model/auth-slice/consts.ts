import {AuthState} from './state.ts';

export const initialState: AuthState = {
  authorized: undefined,
  currentUser: null,
  jwtPayload: null,
  userRole: undefined,
  needRoleChecking: false,
  needTokenRefresh: false
};
