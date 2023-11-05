import { PropsWithChildren } from 'react';

export type TableRowProps = {
  name: string;
  balance: string;
  total?: string | number;
  //price?: string | number
} & PropsWithChildren;
