import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {AuthTokenService} from '../../../../../5_features/auth';
import {BASE_BACKEND_URL} from '../../basic/config.ts';
import {addAuthHeader} from '../headers/process-headers.ts';
import {createTypedApiFunction} from '../../../infrastructure/create-api.ts';
import {HookDefinitions} from './hook-definitions.ts';
import {SchoolClassesResponse} from '../backend-types/nutrition/school-classes.ts';
import {SchoolClass} from '../frontend-types/nutrition/school-class.ts';
import {Mealtime} from '../frontend-types/nutrition/mealtime.ts';

export const Api = createTypedApiFunction<HookDefinitions>()({
  reducerPath: 'api/v3',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL,
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getAuthToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: (builder) => ({
    getSchoolClasses: builder.query({
      query: (params) => ({
        url: '/nutrition/v1/school-classes',
        params: params
      }),
      transformResponse: (responseData: SchoolClassesResponse): SchoolClass[] =>
        responseData.map(schoolClass => ({
          id: schoolClass.id,
          teacherId: schoolClass.teacherId,
          number: schoolClass.number,
          literal: schoolClass.literal,
          mealtimes: schoolClass.mealtimes.map(mealtime => Mealtime[mealtime])
        }))
    })
  })
});

export const {
  useGetSchoolClassesQuery
} = Api;
