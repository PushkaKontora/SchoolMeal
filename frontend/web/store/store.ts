import {configureStore} from '@reduxjs/toolkit';
import {setupListeners} from '@reduxjs/toolkit/query';
import {featuresMiddlewares} from '../src/5_features/reducer';
import {entitiesMiddlewares} from '../src/6_entities/reducer';
import authSlice from '../src/5_features/auth/model/auth-slice/auth-slice';
import {AUTH_API} from '../src/5_features/auth';
import {USER_API} from '../src/6_entities/user';

const middleware = [
  ...featuresMiddlewares,
  ...entitiesMiddlewares
];

export const store = configureStore({
  reducer: {
    auth: authSlice,
    [AUTH_API.reducerPath]: AUTH_API.reducer,
    [USER_API.reducerPath]: USER_API.reducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(middleware)
});

setupListeners(store.dispatch);