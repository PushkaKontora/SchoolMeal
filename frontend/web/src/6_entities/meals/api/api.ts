import {createApi} from '@reduxjs/toolkit/query/react';
import {CONFIG} from './config';

export const MEAL_REQUESTS_API = createApi(CONFIG);
export const {useGetMealRequestsQuery} = MEAL_REQUESTS_API;
