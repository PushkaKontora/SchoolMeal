import {PropsWithChildren} from 'react';

export type SidebarIconedButtonProps = {
  text: string,
  onClick: () => void,
  active?: boolean
} & PropsWithChildren;
