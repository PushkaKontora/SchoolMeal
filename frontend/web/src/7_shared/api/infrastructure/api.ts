import {HooksTypeV3, HooksV3, MiddlewaresV3, ReducersV3} from '../implementations/v3';

export const APIS: {
  current: HooksTypeV3,
  v1: object
} = {
  current: HooksV3,
  v1: {}
};

export const API_REDUCERS = {
  ...ReducersV3
};

export const API_MIDDLEWARES = [
  ...MiddlewaresV3
];
