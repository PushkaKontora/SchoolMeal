import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/deprecated/config.ts';
import {RegisterBody} from './types';
import {User} from '../model/user';
import {AuthTokenProcessor} from '../../../7_shared/lib/auth';
import {ConfigSettings} from '../../../7_shared/api/deprecated/types.ts';
import {addAuthHeader} from '../../../7_shared/api/deprecated/procces-headers.ts';

export enum Tags {
  User = 'User'
}

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/users',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/users',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenProcessor.getAuthToken();
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