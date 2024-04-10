import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {AuthTokenProcessor} from '../../../../../5_features/auth';
import {BASE_BACKEND_URL} from '../../basic/config.ts';
import {addAuthHeader} from '../headers/process-headers.ts';
import {createTypedApiFunction} from '../../../infrastructure/create-api.ts';
import {HookDefinitions} from './hook-definitions.ts';
import {GetSchoolClassesParams} from '../backend-types/nutrition/school-classes.ts';
import {Mealtime} from '../frontend-types/nutrition/mealtime.ts';
import {
  GetNutritionRequestParams,
  SubmitNutritionRequestBody
} from '../backend-types/nutrition/requests.ts';
import {dateToISOWithoutTime} from '../../../../lib/date';
import {GetPupilsParams, ResumedPupilOut} from '../backend-types/nutrition/pupils.ts';
import {toNutritionRequest} from '../mappers/nutrition-request.ts';
import {toSchoolClassArray} from '../mappers/school-class.ts';
import {GetPortionsParams} from '../backend-types/nutrition/portions.ts';
import {toPortionsReport} from '../mappers/portions.ts';
import {toPupilArray} from '../mappers/pupil.ts';

export const Api = createTypedApiFunction<HookDefinitions>()({
  reducerPath: 'api/v3',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL,
    prepareHeaders: async (headers) => {
      const token = await AuthTokenProcessor.getAuthToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getSchoolClasses: builder.query({
      query: (params) => ({
        url: '/nutrition/v1/school-classes',
        params: {
          teacher_id: params.teacherId
        } as GetSchoolClassesParams
      }),
      transformResponse: toSchoolClassArray
    }),
    getNutritionRequest: builder.query({
      query: (frontendParams) => ({
        url: '/nutrition/v1/requests',
        params: {
          class_id: frontendParams.classId,
          on_date: dateToISOWithoutTime(frontendParams.date)
        } as GetNutritionRequestParams
      }),
      transformResponse: toNutritionRequest
    }),
    sendNutritionRequest: builder.mutation({
      query: (body) => ({
        url: '/nutrition/v1/requests',
        body: {
          classId: body.classId,
          onDate: dateToISOWithoutTime(body.date),
          overrides: body.overrides.map<ResumedPupilOut>(pupil => ({
            id: pupil.id,
            mealtimes: pupil.mealtimes.map(mealtime => Mealtime[mealtime])
          }))
        } as SubmitNutritionRequestBody
      })
    }),
    prefillNutritionRequest: builder.query({
      query: (params) => ({
        url: '/nutrition/v1/requests/prefill',
        params: {
          class_id: params.classId,
          on_date: dateToISOWithoutTime(params.date)
        } as GetNutritionRequestParams
      }),
      transformResponse: toNutritionRequest
    }),
    getPortions: builder.query({
      query: (params) => ({
        url: '/nutrition/v1/portions',
        params: {
          class_type: params.classType,
          on_date: dateToISOWithoutTime(params.date)
        } as GetPortionsParams
      }),
      transformResponse: toPortionsReport
    }),
    getPupils: builder.query({
      query: (params) => ({
        url: '/nutrition/v1/pupils',
        params: {
          class_id: params.classId,
          parent_id: params.parentId
        } as GetPupilsParams
      }),
      transformResponse: toPupilArray
    })
  })
});

export const {
  useGetSchoolClassesQuery,
  useGetNutritionRequestQuery,
  useSendNutritionRequestMutation,
  usePrefillNutritionRequestQuery,
  useGetPortionsQuery,
  useGetPupilsQuery
} = Api;