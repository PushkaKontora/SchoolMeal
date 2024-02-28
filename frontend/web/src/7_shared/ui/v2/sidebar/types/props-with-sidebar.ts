import {Sidebar, SidebarProps} from '../sidebar';
import {ReactElement} from 'react';

export type PropsWithSidebar = {
  sidebar: ReactElement<SidebarProps, typeof Sidebar>
}
