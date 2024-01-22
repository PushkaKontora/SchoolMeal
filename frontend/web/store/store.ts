import {configureStore} from '@reduxjs/toolkit';
import {setupListeners} from '@reduxjs/toolkit/query';
import {featuresMiddlewares} from '../src/5_features/reducer';
import {entitiesMiddlewares} from '../src/6_entities/reducer';
import authSlice from '../src/5_features/auth/model/auth-slice/auth-slice';
import {AUTH_API} from '../src/5_features/auth';
import {USER_API} from '../src/6_entities/user';
import {MEAL_REQUESTS_API} from '../src/6_entities/meals/api/api';
import {REQUESTS_API} from '../src/6_entities/requests/api/api.ts';

const middleware = [
  ...featuresMiddlewares,
  ...entitiesMiddlewares
];

export const store = configureStore({
  reducer: {
    auth: authSlice,
    [AUTH_API.reducerPath]: AUTH_API.reducer,
    [USER_API.reducerPath]: USER_API.reducer,
    [MEAL_REQUESTS_API.reducerPath]: MEAL_REQUESTS_API.reducer,
    [REQUESTS_API.reducerPath]: REQUESTS_API.reducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(middleware)
});

setupListeners(store.dispatch);
