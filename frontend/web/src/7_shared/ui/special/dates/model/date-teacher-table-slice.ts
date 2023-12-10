import { createSlice } from '@reduxjs/toolkit';

export interface DateTeacherTableState {
  currentDate: string;
}

const DATE_STRING = new Date();

const initialState: DateTeacherTableState = {
  currentDate: DATE_STRING.toString(),
};

export const dateTeacherTableSlice = createSlice({
  name: 'dateTeacherTable',
  initialState,
  reducers: {
    selectionNewDate: (state, action) => {
      state.currentDate = action.payload.currentDate;
    },
  },
});

// Action creators are generated for each case reducer function
export const { selectionNewDate } = dateTeacherTableSlice.actions;

export default dateTeacherTableSlice.reducer;
