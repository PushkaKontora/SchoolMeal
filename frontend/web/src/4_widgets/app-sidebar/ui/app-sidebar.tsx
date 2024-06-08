import {Sidebar} from '../../../7_shared/ui/v2/sidebar';
import {AppSidebarProps} from '../model/props.ts';

import ExitIcon from '../../../2_processes/role-sidebar/role-sidebar/assets/exit.svg?react';

export function AppSidebar(props: AppSidebarProps) {
  return (
    <Sidebar
      selectedItemIndex={props.selectedItemIndex}
      items={props.items}
      actionItems={props.actionItems}
      logoutButtonProps={{
        icon: (
          <ExitIcon/>
        ),
        accountName: props.userName || '',
        onClick: props.onLogoutClick
      }}/>
  );
}
