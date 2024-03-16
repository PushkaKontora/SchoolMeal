import {CSSProperties, PropsWithChildren, ReactElement} from 'react';

export type ContentStyles = {
  padding: CSSProperties['padding']
}

export type SidebarWithContentProps = {
  sidebarWidth?: string,
  contentStyles?: ContentStyles,
  shouldShowSidebar?: boolean,
  sidebar: ReactElement
} & PropsWithChildren;
