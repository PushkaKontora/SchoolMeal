import {BaseQueryFn} from '@reduxjs/toolkit/src/query/baseQueryTypes.ts';
import {MutationDefinition, QueryDefinition} from '@reduxjs/toolkit/dist/query/react';
import {LoginBody, LoginResponse} from '../backend-types/user-management/login.ts';
import {RefreshBody, RefreshResponse} from '../backend-types/user-management/refresh.ts';
import {OkSchema} from '../backend-types/universal/ok-schema.ts';
import {GetSchoolClassesParams, SchoolClass} from '../frontend-types/nutrition/school-class.ts';
import {
  GetNutritionRequestParams,
  NutritionRequest,
  SubmitNutritionRequestBody
} from '../frontend-types/nutrition/nutrition-request.ts';
import {GetPortionsParams, PortionsReport} from '../frontend-types/nutrition/portions.ts';
import {GetPupilsParams, PupilsResponse} from '../frontend-types/nutrition/pupil.ts';

export type AuthHookDefinitions<
  B extends BaseQueryFn = BaseQueryFn,
  T extends string = string
> = {
  login: MutationDefinition<LoginBody, B, T, LoginResponse>,
  refresh: MutationDefinition<RefreshBody, B, T, RefreshResponse>,
  logout: MutationDefinition<void, B, T, OkSchema>
}

export type HookDefinitions<
  B extends BaseQueryFn = BaseQueryFn,
  T extends string = string
> = {
  getSchoolClasses: QueryDefinition<GetSchoolClassesParams, B, T, SchoolClass[]>,
  getNutritionRequest: QueryDefinition<GetNutritionRequestParams, B, T, NutritionRequest>,
  sendNutritionRequest: MutationDefinition<SubmitNutritionRequestBody, B, T, OkSchema>,
  prefillNutritionRequest: QueryDefinition<GetNutritionRequestParams, B, T, NutritionRequest>,
  getPortions: QueryDefinition<GetPortionsParams, B, T, PortionsReport>,
  getPupils: QueryDefinition<GetPupilsParams, B, T, PupilsResponse>
}
