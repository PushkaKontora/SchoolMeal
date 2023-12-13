import {createApi} from '@reduxjs/toolkit/query/react';
import {CONFIG} from './config';

export const NUTRITION_API = createApi(CONFIG);

export const {useGetPupilNutritionQuery,
  useChangeNutritionPlanMutation,
  useCancelNutritionMutation,
  useResumeNutritionMutation} = NUTRITION_API;

