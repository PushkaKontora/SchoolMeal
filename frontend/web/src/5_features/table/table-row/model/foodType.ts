import { PropsWithChildren } from 'react';

export type FoodType = {
  isCheck: boolean;
  isDisabled: boolean;
} & PropsWithChildren;
