import {createSlice, PayloadAction} from '@reduxjs/toolkit';
import {initialState} from './consts';
import {JwtPayload} from '../jwt-payload.ts';
import {Role} from '../role.ts';
import {RequestedAction} from './actions.ts';

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuthorized(state, action) {
      state.authorized = action.payload;
    },
    setUser(state, action) {
      state.currentUser = action.payload;
    },
    setUserRole(state, action) {
      state.userRole = action.payload;
    },
    setJwtPayload(state, action) {
      state.jwtPayload = action.payload;
    },
    authenticate(state, action: PayloadAction<{
      userRole: Role,
      jwtPayload: JwtPayload
    }>) {
      state.authorized = true;
      state.userRole = action.payload.userRole;
      state.jwtPayload = action.payload.jwtPayload;
    },
    logout(state) {
      state.authorized = false;
      state.userRole = undefined;
      state.jwtPayload = null;
      state.currentUser = null;
    },
    requestRoleChecking(state) {
      state.needRoleChecking = true;
    },
    requestTokenRefresh(state) {
      state.needTokenRefresh = true;
    }
  }
});
