import { PropsWithChildren } from 'react';
import { FoodType } from './foodType';

export type TableRowProps = {
  name: string;
  balance: string;
  total?: string | number;
  breakfast: FoodType,
  lunch: FoodType,
  snack: FoodType,
} & PropsWithChildren;


