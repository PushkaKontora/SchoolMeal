import {addAuthHeader, ConfigSettings, UniversalResponse} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {CancelMealPeriods} from '../../../7_shared/model/cancelMealPeriods';

export const CANCEL_CONFIG: ConfigSettings = {
  reducerPath: 'api/cancel_meals',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/cancel-meal-periods',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    cancelMeal: build.mutation<CancelMealPeriods, CancelMealPeriods>({
      query: (body) => ({
        url: '',
        method: 'POST',
        body: body
      })
    }),
    deleteCanceledMeal: build.mutation<UniversalResponse, number>({
      query: (periodId) => ({
        url: `/${periodId}`,
        method: 'DELETE'
      })
    })
  })
};
