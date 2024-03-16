import {User} from '../../../7_shared/model/user.ts';
import {SidebarIconedButtonProps} from '../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

export type AppSidebarProps= {
  selectedItemIndex: number,
  currentUser?: User,
  items: SidebarIconedButtonProps[]
}
