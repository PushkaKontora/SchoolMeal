import {createTypedApiFunction} from '../../../infrastructure/create-api.ts';
import {AuthHookDefinitions} from './hook-definitions.ts';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../basic/config.ts';

export const AuthApi = createTypedApiFunction<AuthHookDefinitions>()({
  reducerPath: 'api/v3/auth-forms',
  baseQuery: fetchBaseQuery({
    baseUrl: `${BASE_BACKEND_URL}/user-management`
  }),
  endpoints: builder => ({
    login: builder.mutation({
      query: (body) => ({
        url: '/login',
        method: 'POST',
        body: body
      })
    }),
    refresh: builder.mutation({
      query: (body) => ({
        url: '/refresh',
        method: 'POST',
        body: body
      })
    }),
    logout: builder.mutation({
      query: () => ({
        url: '/logout',
        method: 'POST'
      })
    })
  })
});

export const {
  useLoginMutation,
  useRefreshMutation,
  useLogoutMutation
} = AuthApi;
