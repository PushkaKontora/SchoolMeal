import { PropsWithChildren } from 'react';
import { FoodType } from './foodType';

export type TableRowProps = {
  name: string;
  // balance: string;
  // total?: string | number;
  breakfast: boolean;
  lunch: boolean;
  snack: boolean;
  onChange: (breakfast: boolean, lunch: boolean, snack: boolean) => void;
} & PropsWithChildren;
