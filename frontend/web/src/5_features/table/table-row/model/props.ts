import { PropsWithChildren } from 'react';

export type TableRowProps = {
  name: string;
  balance: string;
  total?: string | number;
  breakfast: true,
  lunch: false,
  snack: false,
} & PropsWithChildren;
