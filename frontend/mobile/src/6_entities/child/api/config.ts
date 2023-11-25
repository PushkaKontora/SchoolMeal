import {addAuthHeader, ConfigSettings, UniversalResponse} from '../../../7_shared/api';
import {fetchBaseQuery} from '@reduxjs/toolkit/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {Child} from '../model/child';
import {ChildMealData, ChildMealDataWithId} from '../model/child-meal-data';
import {MealPlanStatus} from '../model/meal-plan';

export const TAGS = {
  ChildList: 'ChildList'
};

export const CONFIG: ConfigSettings = {
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
    }),
    // роуты-заглушки, будут заменены
    changeMealPlan: build.mutation<ChildMealData, ChildMealDataWithId>({
      queryFn: async (inputData) => {
        return {data: {...inputData }};
      }
    }),
    getChildById: build.query<Child, string>({
      queryFn: async () => {
        return {data: {
          id: 'filler_id',
          firstName: 'Олег',
          lastName: 'Филлеров',
          schoolClass: {
            id: 1,
            school: {
              id: 'filler_school_id',
              name: 'Лучшая школа филлеров'
            },
            number: 12,
            literal: 'АБВ'
          },
          mealPlan: {
            status: MealPlanStatus.Paid
          }
        }
        };
      }
    })
  })
};
