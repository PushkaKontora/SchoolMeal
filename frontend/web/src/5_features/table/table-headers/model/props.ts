import { PropsWithChildren } from 'react';

export type TableHeadersProps = {
  breakfastPrice: string | number;
  lunchPrice: string | number;
  snackPrice: string | number;
} & PropsWithChildren;
