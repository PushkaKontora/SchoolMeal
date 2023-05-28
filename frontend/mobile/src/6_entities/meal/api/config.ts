import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {BASE_BACKEND_URL} from "../../../7_shared/api/config";
import {AuthTokenService} from "../../../5_features/auth";
import {addAuthHeader} from "../../../7_shared/api";
import {Meals} from "../../../7_shared/model/meals";
import {MealsParams} from "./types";

export const MEAL_API = createApi({
    reducerPath: 'api/meal',
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_BACKEND_URL + '/meals',
        prepareHeaders: async (headers, {getState}) => {
            const token = await AuthTokenService.getToken();
            if (token) {
                return addAuthHeader(headers, token);
            }
        }
    }),
    // tagTypes: ['Meals'],
    endpoints: build => ({
        getMeals: build.query<Meals[], MealsParams>({
            query: () => ({
                url: ''
            }),
            // providesTags: (result) =>
            //     result
            //         ? [
            //             ...result.map(({id}) => ({type: 'UserChildren', id} as const)),
            //             {type: 'Meals', id: 'LIST'},
            //         ]
            //         : [{type: 'Meals', id: 'LIST'}],
        })
    })
});

export const {useGetUserMealsQuery} = MEAL_API;