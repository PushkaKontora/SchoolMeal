import {USER_API} from '../user';
import {Middleware} from '@reduxjs/toolkit';

export const entitiesMiddlewares = [
    USER_API.middleware as Middleware,
];
