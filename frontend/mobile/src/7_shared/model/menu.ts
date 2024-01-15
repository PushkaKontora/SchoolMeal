import {Portions} from './portions';
import {UUID} from './uuid';
import {Food} from './food';

export type LegacyMenu = {
    'price': number,
    'portions': Portions[],
}

export type Menu = {
    id: UUID,
    date: string,
    breakfast: {
        foods: Food[],
        cost: string
    },
    dinner: {
        foods: Food[],
        cost: string
    },
    snacks: {
        foods: Food[],
        cost: string
    }
}
