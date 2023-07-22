import {AUTH_API} from '../auth';
import {Middleware} from '@reduxjs/toolkit';

export const featuresMiddlewares = [
  AUTH_API.middleware as Middleware
];
