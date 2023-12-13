import {createApi} from '@reduxjs/toolkit/query/react';
import {CONFIG} from './config';

export const CHILD_API = createApi(CONFIG);

// useGetUserChildQuery, useFindChildOnIDMutation, useChangeMealPlanMutation, useGetChildByIdQuery
export const {useGetChildrenQuery, useAddChildMutation} = CHILD_API;