import {configureStore} from '@reduxjs/toolkit';
import {AUTH_API} from '../../5_features/auth';
import {setupListeners} from '@reduxjs/toolkit/query';

export const store = configureStore({
  reducer: {
    [AUTH_API.reducerPath]: AUTH_API.reducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(AUTH_API.middleware)
});

setupListeners(store.dispatch);
