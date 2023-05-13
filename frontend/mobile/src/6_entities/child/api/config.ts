import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {BASE_BACKEND_URL} from "../../../7_shared/api/config";
import {Child} from "../model/child";
import {FindChildBody} from "./types";

export const CHILD_API = createApi({
    reducerPath: 'api/children',
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_BACKEND_URL + '/children'
    }),
    tagTypes: ['UserChildren'],
    endpoints: build => ({
        findChildOnID: build.mutation<Child, FindChildBody>({
            query: (body) => ({
                url: '',
                method: 'POST',
                body: body,
            }),
            invalidatesTags: [{type: 'UserChildren', id: 'LIST'}]
        }),
        getUserChild: build.query<Child[], void>({
            query: () => ({
                url: '/'
            }),
            providesTags: (result) =>
                result
                    ? [
                        ...result.map(({ id }) => ({ type: 'UserChildren' as const, id })),
                        { type: 'UserChildren', id: 'LIST' },
                    ]
                    : [{ type: 'UserChildren', id: 'LIST' }],
        })
    })
});

export const {useGetUserChildQuery, useFindChildOnIDMutation} = CHILD_API;