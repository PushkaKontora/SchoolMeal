import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {BASE_BACKEND_URL} from "../../../7_shared/api/config";
import {Child} from "../model/child";
import {FindChildBody} from "./types";
import {AuthTokenService} from "../../../5_features/auth";
import {addAuthHeader} from "../../../7_shared/api";

export const CHILD_API = createApi({
    reducerPath: 'api/children',
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_BACKEND_URL + '/child',
        prepareHeaders: async (headers, {getState}) => {
            const token = await AuthTokenService.getToken();
            if (token) {
                return addAuthHeader(headers, token);
            }
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
            invalidatesTags: (result, error) => [{type: 'UserChildren'}],
        }),
        getUserChild: build.query<Child[], void>({
            query: () => ({
                url: ''
            }),
            providesTags: (result) =>
                result
                    ? [
                        ...result.map(({id}) => ({type: 'UserChildren', id} as const)),
                        {type: 'UserChildren', id: 'LIST'},
                    ]
                    : [{type: 'UserChildren', id: 'LIST'}],
        })
    })
});

export const {useGetUserChildQuery, useFindChildOnIDMutation} = CHILD_API;