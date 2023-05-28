import {USER_API} from '../user';
import {Middleware} from '@reduxjs/toolkit';
import {CHILD_API} from "../child/api/config";
import {MEAL_API} from '../meal/api/api';

export const entitiesMiddlewares = [
    USER_API.middleware as Middleware,
    CHILD_API.middleware as Middleware
    MEAL_API.middleware as Middleware
];
