import {BaseQueryFn} from '@reduxjs/toolkit/src/query/baseQueryTypes.ts';
import {createApi} from '@reduxjs/toolkit/query/react';
import {EndpointDefinitions} from '@reduxjs/toolkit/query/react';

export function createTypedApiFunction<
  Definitions extends EndpointDefinitions,
  BaseQueryType extends BaseQueryFn = BaseQueryFn,
  Name extends string = string,
  Tags extends string = string>() {
  return (createApi<BaseQueryType, Definitions, Name, Tags>);
}
