
import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { featuresMiddlewares } from '../src/5_features/reducer';
import { entitiesMiddlewares } from '../src/6_entities/reducer';
import authSlice from '../src/5_features/auth/model/auth-slice/auth-slice';

import { AUTH_API } from '../src/5_features/auth';
import { USER_API } from '../src/6_entities/user';
import { NUTRITION_API } from '../src/6_entities/nutrition';
import { MEAL_REQUESTS_API } from '../src/6_entities/meals/api/api';
import checkboxSlice from '../src/5_features/table/model/checkbox-slice.ts/checkbox-slice';
import classTabsSlice from '../src/5_features/tabs/class-selection/model/class-tabs-slice';
import dateTeacherTableSlice from '../src/7_shared/ui/special/dates/model/date-teacher-table-slice';
import {REQUESTS_API} from '../src/6_entities/requests/api/api.ts';

];

export const store = configureStore({
  reducer: {
    auth: authSlice,
    checkbox: checkboxSlice,
    classTabs: classTabsSlice,
    dateTeacherTable: dateTeacherTableSlice,
    [AUTH_API.reducerPath]: AUTH_API.reducer,
    [USER_API.reducerPath]: USER_API.reducer,
    [NUTRITION_API.reducerPath]: NUTRITION_API.reducer,
    [REQUESTS_API.reducerPath]: REQUESTS_API.reducer  },
      .concat(middleware)
});

setupListeners(store.dispatch);
