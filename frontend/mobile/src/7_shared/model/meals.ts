import {Menu} from "./menu";

export type Meals = {
    "id": number,
    "classId": number,
    "date": string,
    "menu": {
        "breakfast"?: Menu,
        "lunch"?: Menu,
        "dinner"?: Menu
    }
}