import {createApi} from '@reduxjs/toolkit/query/react';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/deprecated/config.ts';
import {AuthTokenProcessor} from '../../../7_shared/lib/auth';
import {addAuthHeader} from '../../../7_shared/api';
import {RequestReport, RequestReportIn} from './types.ts';

export const REQUESTS_API = createApi({
  reducerPath: 'api/requests',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/requests',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenProcessor.getAuthToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    getReport: build.query<RequestReport, RequestReportIn>({
      query: (data) => ({
        url: '/report',
        params: {
          class_type: data.classType,
          on_date: data.date
        }
      })
    })
  })
});

export const {useGetReportQuery} = REQUESTS_API;
