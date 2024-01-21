import {createApi} from '@reduxjs/toolkit/query/react';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {addAuthHeader} from '../../../7_shared/api';
import {User} from '../model/user';
import {RegisterBody} from './types';

export const USER_API = createApi({
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
  tagTypes: ['User'],
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
});

export const {useCurrentUserQuery, useRegisterMutation} = USER_API;
