import {addAuthHeader, ConfigSettings, UniversalResponse} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {FeedbackData} from './types';

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/feedback',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/canteens',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    createFeedback: build.mutation<UniversalResponse, FeedbackData>({
      query: (feedbackData) => ({
        url: `/${feedbackData.canteenId}/feedbacks`,
        method: 'POST',
        body: {
          text: feedbackData.text
        }
      })
    })
  })
};
