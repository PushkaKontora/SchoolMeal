import {SidebarIconedButtonProps} from '../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

export type AppSidebarProps= {
  selectedItemIndex: number,
  userName?: string,
  items: SidebarIconedButtonProps[]
  actionItems?: SidebarIconedButtonProps[]
}
