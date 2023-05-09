import {configureStore} from '@reduxjs/toolkit';
import {AUTH_API} from '../../5_features/auth';
import {setupListeners} from '@reduxjs/toolkit/query';
import {CHILD_API} from "../../6_entities/child/api/config";

export const store = configureStore({
    reducer: {
        [AUTH_API.reducerPath]: AUTH_API.reducer,
        [CHILD_API.reducerPath]: CHILD_API.reducer,
    },
    middleware: getDefaultMiddleware =>
        getDefaultMiddleware()
            // .concat(AUTH_API.middleware)
            .concat(CHILD_API.middleware)
});

setupListeners(store.dispatch);
