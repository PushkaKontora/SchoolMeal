import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { addAuthHeader } from '../../../7_shared/api';
import { BASE_BACKEND_URL } from '../../../7_shared/api/config';
import { AuthTokenService } from '../../../5_features/auth';
import { SchoolClasses } from '../model/schoolClasses';
import { PlanReport } from '../model/PlanReport';
import { RegisterBody } from '../model/RegisterBody';

export enum Tags {
  Nutrition = 'Nutrition',
}

export const NUTRITION_API = createApi({
  reducerPath: 'api/nutrition',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL,
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    },
  }),
  tagTypes: Object.values(Tags),
  endpoints: (builder) => ({
    requestPrepare: builder.mutation<void, RegisterBody>({
      query: (body) => ({
        url: 'requests/prepare',
        method: 'POST',
        body: body,
      }),
    }),
    schoolClasses: builder.query<SchoolClasses[], string>({
      query: (teacher_id) => {
        return {
          url: '/school-classes',
          params: { teacher_id },
        };
      },
    }),
    pupils: builder.query<PlanReport, { class_id: string; on_date: string }>({
      query: (data) => {
        return {
          url: '/requests/plan-report',
          params: { ...data },
        };
      },
    }),
  }),
});

export const {
  useSchoolClassesQuery,
  usePupilsQuery,
  useRequestPrepareMutation,
} = NUTRITION_API;

// + '/requests'
