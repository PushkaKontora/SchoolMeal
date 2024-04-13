import {AuthApi, useLoginMutation, useLogoutMutation, useRefreshMutation} from './rtk-query/auth-api.ts';
import {
  Api,
  useGetNutritionRequestQuery, useGetPortionsQuery,
  useGetSchoolClassesQuery, usePrefillNutritionRequestQuery,
  useSendNutritionRequestMutation, useGetPupilsQuery,
  useUpdatePupilMealtimesMutation, useGetNotificationsQuery,
  useReadNotificationsMutation
} from './rtk-query/api.ts';
import {Middleware} from '@reduxjs/toolkit';

export const HooksV3 = {
  // AuthApi
  useLoginMutation,
  useRefreshMutation,
  useLogoutMutation,
  // Api
  useGetSchoolClassesQuery,
  useGetNutritionRequestQuery,
  useSendNutritionRequestMutation,
  usePrefillNutritionRequestQuery,
  useGetPortionsQuery,
  useGetPupilsQuery,
  useUpdatePupilMealtimesMutation,
  useGetNotificationsQuery,
  useReadNotificationsMutation
};

export type HooksTypeV3 = typeof HooksV3;

export const ReducersV3 = {
  [Api.reducerPath]: Api.reducer,
  [AuthApi.reducerPath]: AuthApi.reducer
};

export const MiddlewaresV3 = [
  Api.middleware as Middleware,
  AuthApi.middleware as Middleware
];
