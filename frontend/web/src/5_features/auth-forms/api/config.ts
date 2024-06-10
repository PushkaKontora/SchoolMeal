import {UniversalResponse} from '../../../7_shared/api/deprecated/api.ts';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/deprecated/config.ts';
import {SignInBody, TokenResponse} from './types';
import {ConfigSettings} from '../../../7_shared/api/deprecated/types.ts';

/**
 * @deprecated
 */
export enum Tags {
  User = 'User'
}

/**
 * @deprecated
 */
export const CONFIG: ConfigSettings = {
  reducerPath: 'api/auth-forms',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/users'
  }),
  tagTypes: Object.values(Tags),
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
};