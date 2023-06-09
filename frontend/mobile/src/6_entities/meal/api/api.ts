import {createApi} from '@reduxjs/toolkit/query/react';
import {CANCEL_CONFIG} from './config';

export const MEAL_CANCEL_API = createApi(CANCEL_CONFIG);
export const {useCancelMealMutation, useDeleteCanceledMealMutation} = MEAL_CANCEL_API;
