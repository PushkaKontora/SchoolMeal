import {createApi} from '@reduxjs/toolkit/query/react';
import {CONFIG} from './config';

export const USER_API = createApi(CONFIG);
export const {useCurrentUserQuery, useRegisterMutation} = USER_API;