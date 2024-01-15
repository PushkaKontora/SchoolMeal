import {LegacyMenu} from './menu';

export type Meals = {
    'id': number,
    'classId': number,
    'date': string,
    'menu': {
        'breakfast'?: LegacyMenu,
        'lunch'?: LegacyMenu,
        'dinner'?: LegacyMenu
    }
}