import {authSlice} from './auth-slice.ts';

export const {
  setAuthorized,
  setUser,
  setJwtPayload,
  setUserRole,
  authenticate,
  logout
} = authSlice.actions;

export {authSlice} from './auth-slice.ts';
