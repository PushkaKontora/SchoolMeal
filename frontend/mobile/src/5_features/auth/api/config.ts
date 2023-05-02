import {ConfigSettings, UniversalResponse} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {SignInBody, TokenResponse} from './types';

export enum Tags {

}

export const CONFIG: ConfigSettings = {
  reducerPath: 'api/auth',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/auth'
  }),
  tagTypes: Object.values(Tags),
  endpoints: build => ({
    signIn: build.mutation<TokenResponse, SignInBody>({
      query: (body) => ({
        url: '/signin',
        method: 'POST',
        body: body,
      })
    }),
    logout: build.mutation<UniversalResponse, undefined>({
      query: () => ({
        url: '/logout',
        method: 'POST'
      })
    }),
    refreshTokens: build.mutation<TokenResponse, undefined>({
      query: () => ({
        url: '/refresh-tokens',
        method: 'POST'
      })
    })
  })
};
