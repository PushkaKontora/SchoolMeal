import {addAuthHeader} from '../../../../7_shared/api';
import {BASE_BACKEND_URL} from '../../../../7_shared/api/config';
import {AuthTokenService} from '../../../../5_features/auth';

import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {Meals} from '../../../../7_shared/model/meals';
import {MealsParams} from './types';
import {createApi} from '@reduxjs/toolkit/query/react';

export const MEAL_API = createApi({
  reducerPath: 'api/meals',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/meals',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    getMeals: build.query<Meals[], MealsParams>({
      query: (data) => ({
        url: '/',
        params: data,
      }),
      // providesTags: (result) =>
      //     result
      //         ? [
      //             ...result.map(({id}) => ({type: 'UserChildren', id} as const)),
      //             {type: 'Meals', id: 'LIST'},
      //         ]
      //         : [{type: 'Meals', id: 'LIST'}],
    })
  })
});

export const {useGetMealsQuery} = MEAL_API;
