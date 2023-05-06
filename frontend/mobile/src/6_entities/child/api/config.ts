import {ConfigSettings} from "../../../7_shared/api";
import {fetchBaseQuery} from "@reduxjs/toolkit/dist/query/react";
import {BASE_BACKEND_URL} from "../../../7_shared/api/config";
import {User} from "../../user";
import {RegisterBody} from "../../user/api/types";
import {Tags} from "../../user/api/config";

export const CONFIG: ConfigSettings = {
    reducerPath: 'api/users',
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_BACKEND_URL + '/users'
    }),
    tagTypes: Object.values(Tags),
    endpoints: build => ({
        register: build.mutation<User, RegisterBody>({
            query: (body) => ({
                url: '',
                method: 'POST',
                body: body,
            })
        }),
        currentUser: build.query<User, undefined>({
            query: () => ({
                url: '/me'
            })
        })
    })
};