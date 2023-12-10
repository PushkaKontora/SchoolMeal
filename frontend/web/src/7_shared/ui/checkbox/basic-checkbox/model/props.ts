import { PropsWithChildren } from 'react';

export type BasicCheckboxProps = {
  isDisable: boolean;
  isCheck: boolean;
  onChange?: (state: boolean) => void;
  type: string;
  isHeader: boolean;
  //'b'|| 'l'||'s'
} & PropsWithChildren;
