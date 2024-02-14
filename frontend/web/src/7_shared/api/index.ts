import {Api} from './api.ts';

export {addAuthHeader} from './procces-headers';
export type {ConfigSettings, UniversalResponse} from './types';

export * from './api.ts';
export const ApiMiddleware = Api.middleware;
