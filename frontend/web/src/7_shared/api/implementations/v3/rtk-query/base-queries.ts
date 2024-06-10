import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../basic/config.ts';
import {AuthTokenProcessor} from '../../../../lib/auth';
import {addAuthHeader} from '../headers/process-headers.ts';
import {BaseQueryFn, FetchArgs, FetchBaseQueryError} from '@reduxjs/toolkit/dist/query/react';
import {FingerprintOut} from '../backend-types/user-management/fingerprintOut.ts';
import {RefreshResponse} from '../backend-types/user-management/refresh.ts';
import {logout} from '../../../../lib/auth/model/auth-slice';

const refreshQuery = (body: FingerprintOut) => ({
  url: '/user-management/refresh',
  method: 'POST',
  body: body
});

export const baseQuery = fetchBaseQuery({
  baseUrl: BASE_BACKEND_URL,
  prepareHeaders: async (headers) => {
    const token = AuthTokenProcessor.getAuthToken();

    if (token) {
      return addAuthHeader(headers, token);
    }
    return headers;
  },
  credentials: 'same-origin'
});

export const fetchBaseQueryWithRefresh: BaseQueryFn<
  string | FetchArgs,
  unknown,
  FetchBaseQueryError
> = async (args, api, extra) => {
  const token = AuthTokenProcessor.getAuthToken();
  const payload = AuthTokenProcessor.decodeAuthToken(token);

  if (AuthTokenProcessor.isTokenExpired(payload)) {
    const refreshResult = await baseQuery(refreshQuery({
      fingerprint: 'aaaaa'
    }), api, extra);

    if (refreshResult.data) {
      const data = refreshResult.data as RefreshResponse;
      AuthTokenProcessor.saveAuthToken(data.token);
    } else {
      api.dispatch(logout());
      return {error: {
        status: 403, data: 'Unable to refresh token'
      }};
    }
  }

  return baseQuery(args, api, extra);
};
