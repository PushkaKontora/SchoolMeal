import {createSlice} from '@reduxjs/toolkit';
import {initialState} from './consts';

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuthorized(state, action) {
      state.authorized = action.payload;
    },
    setUser(state, action) {
      state.currentUser = action.payload;
    }
  }
});

export const {
  setAuthorized,
  setUser
} = authSlice.actions;

export default authSlice.reducer;
