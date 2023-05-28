import {Food} from "./food";

export type Portions = {
    "id": number,
    "food": Food,
    "components": string,
    "weight": number,
    "kcal": number,
    "protein": number,
    "fats": number,
    "carbs": number,
    "price": number
}