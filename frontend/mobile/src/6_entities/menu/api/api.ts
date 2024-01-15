import {createApi} from '@reduxjs/toolkit/query/react';
import {fetchBaseQuery} from '@reduxjs/toolkit/dist/query/react';
import {BASE_BACKEND_URL} from '../../../7_shared/api/config';
import {AuthTokenService} from '../../../5_features/auth';
import {addAuthHeader} from '../../../7_shared/api';
import {Menu} from '../../../7_shared/model/menu';
import {GetMenuIn} from './types';

export const MENU_API = createApi({
  reducerPath: 'api/menu',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_BACKEND_URL + '/menu',
    prepareHeaders: async (headers) => {
      const token = await AuthTokenService.getToken();
      if (token) {
        return addAuthHeader(headers, token);
      }
      return headers;
    }
  }),
  endpoints: build => ({
    getMenu: build.query<Menu, GetMenuIn>({
      query: (data) => ({
        url: '',
        params: {
          school_class_number: data.schoolClassNumber,
          on_date: data.date
        }
      })
    })
  })
});

export const {useGetMenuQuery} = MENU_API;
