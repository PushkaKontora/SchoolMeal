import {addAuthHeader, ConfigSettings} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {RegisterBody} from './types';
import {User} from '../model/user';
import {AuthTokenService} from '../../../5_features/auth';

export enum Tags {
  User = 'User'
}

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/users',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/users',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  tagTypes: Object.values(Tags),
  endpoints: build => ({
    register: build.mutation<User, RegisterBody>({
      query: (body) => ({
        url: 'register-parent',
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['User']
    }),
    currentUser: build.query<User, void>({
      query: () => ({
        url: '/me'
      }),
      providesTags: ['User']
    })
  })
};