import {LegacyFood} from './food';

export type Portions = {
    'id': number,
    'food': LegacyFood,
    'components': string,
    'weight': number,
    'kcal': number,
    'protein': number,
    'fats': number,
    'carbs': number,
    'price': number
}