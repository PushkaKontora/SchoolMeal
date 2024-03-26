/*
import {Api} from './deprecated/api.ts';

export {addAuthHeader} from './deprecated/procces-headers.ts';
export type {ConfigSettings, UniversalResponse} from './deprecated/types.ts';

export * from './deprecated/api.ts';
export config ApiMiddleware = Api.middleware;
*/

export {Api} from './infrastructure';
export {API_MIDDLEWARES, API_REDUCERS} from './infrastructure';
