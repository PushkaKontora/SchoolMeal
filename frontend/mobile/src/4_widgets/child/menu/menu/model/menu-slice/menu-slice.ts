import {createSlice} from '@reduxjs/toolkit';
import {initialState} from './consts';

const menuSlice = createSlice({
  name: 'menu',
  initialState,
  reducers: {
    setDataMenu(state, action) {
      state.dateMeal = action.payload;
    },
  }
});

export const {
  setDataMenu,
} = menuSlice.actions;

export default menuSlice.reducer;
