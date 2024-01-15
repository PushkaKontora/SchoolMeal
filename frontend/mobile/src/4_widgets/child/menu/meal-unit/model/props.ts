import {PropsWithChildren} from 'react';
import {Food} from '../../../../../7_shared/model/food';

export type MealUnitProps = {
    title: string,
    sum: string,
    foods: Food[],
} & PropsWithChildren;
