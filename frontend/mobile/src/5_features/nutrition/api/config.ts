import {addAuthHeader, ConfigSettings, UniversalResponse} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../auth';
import {CancellationPeriod, PupilNutritionInfo} from '../../../7_shared/model/nutrition';
import {CancelNutritionIn, ChangeNutritionPlanIn, ResumeNutritionIn} from './types';

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/nutrition',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/nutrition',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    getPupilNutrition: build.query<PupilNutritionInfo, string>({
      query: (pupilId) => ({
        url: `/${pupilId}`,
        method: 'GET'
      })
    }),
    changeNutritionPlan: build.mutation<UniversalResponse, ChangeNutritionPlanIn>({
      query: (input) => ({
        url: `/${input.pupilId}/plan`,
        method: 'PUT',
        body: input.body
      })
    }),
    cancelNutrition: build.mutation<CancellationPeriod[], CancelNutritionIn>({
      query: (input) => ({
        url: `/${input.pupilId}/cancel`,
        method: 'POST',
        body: input.body
      })
    }),
    resumeNutrition: build.mutation<CancellationPeriod[], ResumeNutritionIn>({
      query: (input) => ({
        url: `/${input.pupilId}/resume`,
        method: 'POST',
        body: input.body
      })
    })
  })
};
