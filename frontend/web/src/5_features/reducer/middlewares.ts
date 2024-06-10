import {AUTH_API} from '../auth-forms';
import {Middleware} from '@reduxjs/toolkit';

export const featuresMiddlewares = [
  AUTH_API.middleware as Middleware
];
