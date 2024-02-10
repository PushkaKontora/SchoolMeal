import {PropsWithChildren, ReactElement} from 'react';

export type SidebarWithContentProps = {
  sidebar: ReactElement,
  sidebarWidth?: string
} & PropsWithChildren;
