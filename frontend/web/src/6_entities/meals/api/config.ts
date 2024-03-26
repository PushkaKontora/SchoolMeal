import {addAuthHeader, ConfigSettings} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/deprecated/config.ts';
import {AuthTokenService} from '../../../5_features/auth';
import {Meal} from '../model/meal';
import {GetMealRequestsParams} from './types';

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/meal-requests',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/meal-requests',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getAuthToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    getMealRequests: build.query<Meal[], GetMealRequestsParams>({
      query: (data) => ({
        url: '',
        params: data
      })
    })
  })
};
