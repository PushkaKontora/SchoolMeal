import {CSSProperties, PropsWithChildren} from 'react';
import {PropsWithSidebar} from '../../types/props-with-sidebar.ts';

export type ContentStyles = {
  padding: CSSProperties['padding']
}

export type SidebarWithContentProps = {
  sidebarWidth?: string,
  contentStyles?: ContentStyles
} & PropsWithChildren
  & PropsWithSidebar;
