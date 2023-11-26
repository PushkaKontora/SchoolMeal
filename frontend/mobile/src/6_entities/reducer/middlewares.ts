import {USER_API} from '../user';
import {Middleware} from '@reduxjs/toolkit';
import {CHILD_API} from '../child/api/api';
import {MEAL_CANCEL_API} from '../meal/api/api';
import {MEAL_API} from '../meal/api/meal-api/config';
import {FEEDBACK_API} from '../feedback';

export const entitiesMiddlewares = [
    USER_API.middleware as Middleware,
    CHILD_API.middleware as Middleware,
    MEAL_API.middleware as Middleware,
    MEAL_CANCEL_API.middleware as Middleware,
    FEEDBACK_API.middleware as Middleware
];
