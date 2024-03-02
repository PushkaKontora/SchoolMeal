import {PropsWithChildren, ReactElement} from 'react';

export type SidebarIconedButtonProps = {
  icon?: ReactElement,
  text: string,
  onClick: () => void,
  active?: boolean
} & PropsWithChildren;
