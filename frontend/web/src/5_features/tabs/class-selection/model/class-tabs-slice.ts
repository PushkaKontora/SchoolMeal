import { createSlice } from '@reduxjs/toolkit';
import { SchoolClasses } from '../../../../6_entities/nutrition/model/schoolClasses';
import { OverridenPupil } from '../../../../6_entities/nutrition/model/RegisterBody';

export interface ClassTabsState {
  activeClass: string;
  classList: string[];
  classID: string;
  allClassList: SchoolClasses[];
  activeClassItemInArray: number | string;
  dataCh: string;
  prepareItems: { [index: string]: OverridenPupil };
  planReportStatus: string;
}

const initialState: ClassTabsState = {
  activeClass: '',
  classList: [],
  classID: '',
  allClassList: [],
  activeClassItemInArray: 0,
  dataCh: '2024-01-23',
  prepareItems: {},
  planReportStatus: 'Не подана',
};

export const classTabsSlice = createSlice({
  name: 'classTabs',
  initialState,
  reducers: {
    selectionClassTabs: (state, action) => {
      state.activeClass = action.payload.activeClass;
      state.classID = action.payload.classID;
      state.activeClassItemInArray = action.payload.activeClassItemInArray;
    },
    fillAvailableClasses: (state, action) => {
      state.classList = action.payload.classList;
      state.activeClass = action.payload.classList[0];
    },
    allTeacherClasses: (state, action) => {
      state.allClassList = action.payload.allClassList;
      state.classID = action.payload.allClassList[0].id;
    },
    getDataCh: (state, action) => {
      state.dataCh = action.payload;
    },
    fillPlanReportStatus: (state, action) => {
      state.planReportStatus = action.payload;
    },
    fillPrepareItems: (state, action) => {
      const pupil: OverridenPupil = action.payload;
      state.prepareItems = {
        ...state.prepareItems,
        [pupil.id]: pupil,
      };
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  selectionClassTabs,
  fillAvailableClasses,
  allTeacherClasses,
  getDataCh,
  fillPrepareItems,
  fillPlanReportStatus,
} = classTabsSlice.actions;

export default classTabsSlice.reducer;
