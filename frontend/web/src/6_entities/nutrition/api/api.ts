import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { addAuthHeader } from '../../../7_shared/api';
import { BASE_BACKEND_URL } from '../../../7_shared/api/config';
import { AuthTokenService } from '../../../5_features/auth';
import { TeacherID } from './types';
import { SchoolClasses } from '../model/schoolClasses';
import { Pupil } from '../../meals/model/pupil-view';

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
    //   register: build.mutation<User, RegisterBody>({
    //     query: (body) => ({
    //       url: 'register-parent',
    //       method: 'POST',
    //       body: body,
    //     }),
    //     invalidatesTags: ['User']
    //   }),
    schoolClasses: builder.query<SchoolClasses[], string>({
      query: (teacher_id) => {
        return {
          url: '/school-classes',
          params: { teacher_id },
        };
      },
    }),
    pupils: builder.query<Pupil[], string>({
      query: (class_id) => {
        return {
          url: '/pupils',
          params: { class_id },
        };
      },
    }),
  }),
});

export const { useSchoolClassesQuery, usePupilsQuery } = NUTRITION_API;

// + '/requests'
