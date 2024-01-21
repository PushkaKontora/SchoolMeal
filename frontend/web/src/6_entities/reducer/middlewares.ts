import { USER_API } from '../user';
import { Middleware } from '@reduxjs/toolkit';
import { MEAL_REQUESTS_API } from '../meals/api/api';
import { NUTRITION_API } from '../nutrition';

export const entitiesMiddlewares = [
  USER_API.middleware as Middleware,
  MEAL_REQUESTS_API.middleware as Middleware,
  NUTRITION_API.middleware as Middleware,
];
