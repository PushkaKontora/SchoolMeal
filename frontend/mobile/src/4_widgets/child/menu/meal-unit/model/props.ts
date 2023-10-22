import {PropsWithChildren} from 'react';
import {Portions} from '../../../../../7_shared/model/portions';

export type MealUnitProps = {
    title: string,
    sum: number,
    portions: Portions[],
} & PropsWithChildren;
