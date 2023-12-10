import { createSlice } from '@reduxjs/toolkit';

export interface ClassTabsState {
  activeClass: string;
  classList: string[];
}

const initialState: ClassTabsState = {
  activeClass: '1А',
  classList: ['1А', '2Б'],
};

export const classTabsSlice = createSlice({
  name: 'classTabs',
  initialState,
  reducers: {
    selectionClassTabs: (state, action) => {
      state.activeClass = action.payload.activeClass;
    },
    fillAvailableClasses: (state, action) => {
      state.classList = action.payload.classList;
      state.activeClass = action.payload.classList[0];
    },
  },
});

// Action creators are generated for each case reducer function
export const { selectionClassTabs, fillAvailableClasses } =
  classTabsSlice.actions;

export default classTabsSlice.reducer;
