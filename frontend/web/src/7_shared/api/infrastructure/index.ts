import {APIS} from './api.ts';

export const Api = {
  ...APIS,
  ...APIS.current
};

export {API_MIDDLEWARES, API_REDUCERS} from './api.ts';
