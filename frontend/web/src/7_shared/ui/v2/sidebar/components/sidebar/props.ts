import {SidebarIconedButtonProps} from '../iconed-button/props.ts';
import {LogoutButtonProps} from '../logout-button';

export type SidebarProps = {
  selectedItemIndex: number,
  items: SidebarIconedButtonProps[],
  actionItems?: SidebarIconedButtonProps[],
  logoutButtonProps: LogoutButtonProps
};
