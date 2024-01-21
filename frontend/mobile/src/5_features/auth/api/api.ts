import {createApi} from '@reduxjs/toolkit/query/react';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {SignInBody, TokenResponse} from './types';
import {UniversalResponse} from '../../../7_shared/api';

export const AUTH_API = createApi({
  reducerPath: 'api/auth',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/users'
  }),
  tagTypes: ['User'],
  endpoints: build => ({
    signIn: build.mutation<TokenResponse, SignInBody>({
      query: (body) => ({
        url: '/authenticate',
        method: 'POST',
        body: body
      }),
      invalidatesTags: ['User'],
      extraOptions: {
        myParam: true
      }
    }),
    logout: build.mutation<UniversalResponse, void>({
      query: () => ({
        url: '/logout',
        method: 'POST'
      })
    }),
    refreshTokens: build.mutation<TokenResponse, void>({
      query: () => ({
        url: '/refresh-tokens',
        method: 'POST'
      })
    })
  })
});
