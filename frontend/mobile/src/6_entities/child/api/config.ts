import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {Child} from '../model/child';
import {FindChildBody} from './types';
import {AuthTokenService} from '../../../5_features/auth';
import {addAuthHeader} from '../../../7_shared/api';
import {ChildMealData, ChildMealDataWithId} from '../types/child-meal-data';

export const CHILD_API = createApi({

  reducerPath: 'api/children',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/children',
    prepareHeaders: async (headers, {getState}) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  tagTypes: ['UserChildren'],
  endpoints: build => ({
    findChildOnID: build.mutation<Child, FindChildBody>({
      query: (body) => ({
        url: '',
        method: 'POST',
        body: body,
      }),
      //  invalidatesTags: [{type: 'UserChildren', id: 'LIST'}]
    }),

    getUserChild: build.query<Child[], void>({
      query: () => ({
        url: ''
      }),
      // providesTags: (result) =>
      //     result
      //         ? [
      //             ...result.map(({ id }) => ({ type: 'UserChildren' as const, id })),
      //             { type: 'UserChildren', id: 'LIST' },
      //         ]
      //         : [{ type: 'UserChildren', id: 'LIST' }],
    }),
    changeMealPlan: build.mutation<ChildMealData, ChildMealDataWithId>({
      query: ({childId, ...body}) => ({
        url: `/${childId}`,
        method: 'PATCH',
        body: body
      })
    }),
    getChildById: build.query<Child, string>({
      query: (childId) => ({
        url: `/${childId}`
      })/*,
      transformResponse(response: Child): Child {
        return transformChild(response);
      }*/
    })
  })
});

export const {useGetUserChildQuery, useFindChildOnIDMutation, useChangeMealPlanMutation, useGetChildByIdQuery} = CHILD_API;