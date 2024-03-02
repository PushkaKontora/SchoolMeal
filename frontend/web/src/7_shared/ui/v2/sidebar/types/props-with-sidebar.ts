import {Sidebar, SidebarProps} from '../components/sidebar';
import {ReactElement} from 'react';

export type PropsWithSidebar = {
  sidebar: ReactElement<SidebarProps, typeof Sidebar>
}
