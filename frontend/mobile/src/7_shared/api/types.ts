import {
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
  FetchBaseQueryMeta
} from '@reduxjs/toolkit/dist/query/react';
import {EndpointBuilder} from '@reduxjs/toolkit/dist/query/endpointDefinitions';

export type ConfigSettings = {
  reducerPath: string,
  baseQuery: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError, object, FetchBaseQueryMeta>,
  tagTypes?: string[],
  endpoints: (build: EndpointBuilder<any, any, any>) => any
};

export type UniversalResponse = {
  msg?: string
}


