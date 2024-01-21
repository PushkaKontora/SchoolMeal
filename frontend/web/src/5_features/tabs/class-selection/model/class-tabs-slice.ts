import { createSlice } from '@reduxjs/toolkit';
import { SchoolClasses } from '../../../../6_entities/nutrition/model/schoolClasses';

export interface ClassTabsState {
  activeClass: string;
  classList: string[];
  classID: string;
  allClassList: SchoolClasses[];
}

const initialState: ClassTabsState = {
  activeClass: '',
  classList: [],
  classID: '',
  allClassList: [],
};

export const classTabsSlice = createSlice({
  name: 'classTabs',
  initialState,
  reducers: {
    selectionClassTabs: (state, action) => {
      state.activeClass = action.payload.activeClass;
      state.classID = action.payload.classID;
    },
    fillAvailableClasses: (state, action) => {
      state.classList = action.payload.classList;
      state.activeClass = action.payload.classList[0];
    },
    allTeacherClasses: (state, action) => {
      state.allClassList = action.payload.allClassList;
      state.classID = action.payload.allClassList[0].id;
    },
  },
});

// Action creators are generated for each case reducer function
export const { selectionClassTabs, fillAvailableClasses, allTeacherClasses } =
  classTabsSlice.actions;

export default classTabsSlice.reducer;
