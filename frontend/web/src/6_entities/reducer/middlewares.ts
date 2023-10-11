import {USER_API} from '../user';
import {Middleware} from '@reduxjs/toolkit';
import {MEAL_REQUESTS_API} from '../meals/api/api';

export const entitiesMiddlewares = [
    USER_API.middleware as Middleware,
    MEAL_REQUESTS_API.middleware as Middleware
];
