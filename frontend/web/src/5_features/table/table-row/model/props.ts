import { PropsWithChildren } from 'react';

export type TableRowProps = {
  name: string;
  // balance: string;
  // total?: string | number;
  breakfast: boolean;
  lunch: boolean;
  snack: boolean;
  onChange: (breakfast: boolean, lunch: boolean, snack: boolean) => void;
} & PropsWithChildren;
