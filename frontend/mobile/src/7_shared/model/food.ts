import {UUID} from './uuid';

export type LegacyFood = {
    'id': number,
    'schoolId': number,
    'name': string,
    'photoPath': string
}

export type Food = {
    id: UUID,
    name: string,
    description: string,
    calories: string,
    proteins: string,
    fats: string,
    carbohydrates: string,
    weight: string,
    price: string,
    photoUrl: string
}
