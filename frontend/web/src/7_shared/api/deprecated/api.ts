import {createApi} from '@reduxjs/toolkit/query/react';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from './config.ts';
import {AuthTokenProcessor} from '../../../5_features/auth';
import {addAuthHeader} from './procces-headers.ts';
import {SchoolClasses} from '../../../6_entities/nutrition/model/schoolClasses.ts';
import {RequestPlanReport} from '../../model/request-report.ts';
import {OverridenPupil, Pupil, } from '../../model/pupil.ts';
import {Menu} from '../../model/menu.ts';
import {UniversalResponse} from './types.ts';
import {User} from '../../model/user.ts';
import {MealRequest} from '../../model/meal-request.ts';
import {ClassType} from '../../model/class-type.ts';

/**
 * @deprecated Устаревший API
 */
export const Api = createApi({
  reducerPath: 'api',
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
  tagTypes: ['PlanningReport'],
  endpoints: (builder) => ({
    getCurrentUser: builder.query<User, void>({
      query: () => ({
        url: '/users/me'
      })
    }),
    getTeacherSchoolClasses: builder.query<SchoolClasses[], string>({
      query: (teacher_id) => ({
        url: '/school-classes',
        params: { teacher_id }
      })
    }),
    getPupils: builder.query<Pupil[], string>({
      query: (class_id) => ({
        url: '/pupils',
        params: { class_id }
      })
    }),
    getMenu: builder.query<Menu, {
      school_class_number: number,
      on_date: string
    }>({
      query: (params) => ({
        url: '/menu',
        params: params
      })
    }),
    getPlanningMealRequest: builder.query<RequestPlanReport, {
      class_id: string,
      on_date: string
    }>({
      query: (params) => ({
        url: '/requests/plan-report',
        params: params
      }),
      providesTags: ['PlanningReport']
    }),
    prepareMealRequest: builder.mutation<UniversalResponse, {
      class_id: string,
      on_date: string,
      overriden_pupils: OverridenPupil[]
    }>({
      query: (body) => ({
        url: '/requests/prepare',
        method: 'POST',
        body: body
      }),
      invalidatesTags: ['PlanningReport']
    }),
    getReport: builder.query<MealRequest, {
      class_type: ClassType,
      on_date: string
    }>({
      query: (params) => ({
        url: 'requests/report',
        params: params
      })
    })
  })
});

/**
 * @deprecated Устаревший API
 */
export const {
  useGetTeacherSchoolClassesQuery,
  useGetPupilsQuery,
  useGetMenuQuery,
  useGetPlanningMealRequestQuery,
  usePrepareMealRequestMutation,
  useGetCurrentUserQuery,
  useGetReportQuery
} = Api;
