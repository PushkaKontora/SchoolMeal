import {BaseQueryFn} from '@reduxjs/toolkit/src/query/baseQueryTypes.ts';
import {MutationDefinition, QueryDefinition} from '@reduxjs/toolkit/dist/query/react';
import {GetSchoolClassesParams} from '../backend-types/nutrition/school-classes.ts';
import {LoginBody, LoginResponse} from '../backend-types/user-management/login.ts';
import {RefreshBody, RefreshResponse} from '../backend-types/user-management/refresh.ts';
import {OkSchema} from '../backend-types/universal/ok-schema.ts';
import {SchoolClass} from '../frontend-types/nutrition/school-class.ts';

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
  getSchoolClasses: QueryDefinition<GetSchoolClassesParams, B, T, SchoolClass[]>
}
