import {configureStore, Middleware} from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';

import classTabsSlice from '../src/5_features/tabs/class-selection/model/class-tabs-slice';
import dateTeacherTableSlice from '../src/7_shared/ui/special/dates/model/date-teacher-table-slice';
import {API_MIDDLEWARES, API_REDUCERS} from '../src/7_shared/api';
import {Api} from '../src/7_shared/api/deprecated/api.ts';
import {authSlice} from '../src/7_shared/lib/auth';

const middleware = [
  ...API_MIDDLEWARES,
  Api.middleware as Middleware
];

export const store = configureStore({
  reducer: {
    [authSlice.name]: authSlice.reducer,
    classTabs: classTabsSlice,
    dateTeacherTable: dateTeacherTableSlice,
    /*
    [AUTH_API.reducerPath]: AUTH_API.reducer,
    [USER_API.reducerPath]: USER_API.reducer,
    [MEAL_REQUESTS_API.reducerPath]: MEAL_REQUESTS_API.reducer,
    [NUTRITION_API.reducerPath]: NUTRITION_API.reducer,
    [REQUESTS_API.reducerPath]: REQUESTS_API.reducer,
    */
    ...API_REDUCERS
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(middleware)
});

setupListeners(store.dispatch);