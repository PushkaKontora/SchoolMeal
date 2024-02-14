import {CSSProperties, PropsWithChildren, ReactElement} from 'react';

export type ContentStyles = {
  padding: CSSProperties['padding']
}

export type SidebarWithContentProps = {
  sidebar: ReactElement,
  sidebarWidth?: string,
  contentStyles?: ContentStyles
} & PropsWithChildren;
