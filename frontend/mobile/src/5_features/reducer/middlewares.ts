import {AUTH_API} from '../auth';
import {Middleware} from '@reduxjs/toolkit';
import {NUTRITION_API} from '../nutrition/api';

export const featuresMiddlewares = [
  AUTH_API.middleware as Middleware,
  NUTRITION_API.middleware as Middleware
];
