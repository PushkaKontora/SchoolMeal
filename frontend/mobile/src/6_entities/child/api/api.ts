import {createApi} from '@reduxjs/toolkit/query/react';
import {CONFIG, TAGS} from './config';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {addAuthHeader, UniversalResponse} from '../../../7_shared/api';
import {Child} from '../model/child';

export const CHILD_API = createApi({
  reducerPath: 'api/children',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/children',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  tagTypes: Object.values(TAGS),
  endpoints: build => ({
    getChildren: build.query<Child[], void>({
      query: () => ({
        url: '',
        method: 'GET'
      }),
      providesTags: [TAGS.ChildList]
    }),
    addChild: build.mutation<UniversalResponse, string>({
      query: (childId) => ({
        url: `/${childId}`,
        method: 'POST'
      }),
      invalidatesTags: [TAGS.ChildList]
    })
  })
});

// useGetUserChildQuery, useFindChildOnIDMutation, useChangeMealPlanMutation, useGetChildByIdQuery
export const {useGetChildrenQuery, useAddChildMutation} = CHILD_API;