import { createSlice } from '@reduxjs/toolkit';

export interface CheckboxState {
  value: [boolean, boolean, boolean];
  lastValue: boolean;
  type: string;
  isAction: boolean;
}

const initialState: CheckboxState = {
  value: [false, false, false],
  lastValue: false,
  type: '',
  isAction: false,
};

export const checkboxSlice = createSlice({
  name: 'checkbox',
  initialState,
  reducers: {
    changeStateCheckbox: (state, action) => {
      state.type = action.payload.type;
      state.lastValue = action.payload.value;

      if (action.payload.type == 'b') {
        state.value[0] = action.payload.value;
      }

      if (action.payload.type == 'l') {
        state.value[1] = action.payload.value;
      }

      if (action.payload.type == 's') {
        state.value[2] = action.payload.value;
      }

      state.isAction = !state.isAction;
    },
  },
});

// Action creators are generated for each case reducer function
export const { changeStateCheckbox } = checkboxSlice.actions;

export default checkboxSlice.reducer;
