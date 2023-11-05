import { PropsWithChildren } from 'react';

export type BasicCheckboxProps = {
  isDisable: boolean;
  isCheck?: boolean;
} & PropsWithChildren;
