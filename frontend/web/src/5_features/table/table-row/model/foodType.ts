import { PropsWithChildren } from 'react';

export type FoodType = {
  isCheck: boolean;
  isDisabled: boolean;
  price: number;
} & PropsWithChildren;
