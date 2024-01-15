import {configureStore} from '@reduxjs/toolkit';
import {setupListeners} from '@reduxjs/toolkit/query';
import {featuresMiddlewares} from '../src/5_features/reducer';
import {entitiesMiddlewares} from '../src/6_entities/reducer';
import authSlice from '../src/5_features/auth/model/auth-slice/auth-slice';
import {AUTH_API} from '../src/5_features/auth';
import {USER_API} from '../src/6_entities/user';
import {CHILD_API} from '../src/6_entities/child/api/api';
import menuSlice from '../src/4_widgets/child/menu/menu/model/menu-slice/menu-slice';
import {MEAL_CANCEL_API} from '../src/6_entities/meal/api/api';
import {MEAL_API} from '../src/6_entities/meal/api/meal-api/config';
import {FEEDBACK_API} from '../src/6_entities/feedback';
import {NUTRITION_API} from '../src/5_features/nutrition/api';
import middlewares from '../src/1_app/lib/middlewares/error-handler';
import {MENU_API} from '../src/6_entities/menu/api/api';

const middleware = [
  ...middlewares,
  ...featuresMiddlewares,
  ...entitiesMiddlewares
];

export const store = configureStore({
  reducer: {
    auth: authSlice,
    menu: menuSlice,
    [AUTH_API.reducerPath]: AUTH_API.reducer,
    [USER_API.reducerPath]: USER_API.reducer,
    [CHILD_API.reducerPath]: CHILD_API.reducer,
    [MEAL_API.reducerPath]: MEAL_API.reducer,
    [MEAL_CANCEL_API.reducerPath]: MEAL_CANCEL_API.reducer,
    [FEEDBACK_API.reducerPath]: FEEDBACK_API.reducer,
    [NUTRITION_API.reducerPath]: NUTRITION_API.reducer,
    [MENU_API.reducerPath]: MENU_API.reducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(middleware)
});

setupListeners(store.dispatch);
