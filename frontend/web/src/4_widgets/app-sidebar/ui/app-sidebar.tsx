import {Sidebar} from '../../../7_shared/ui/v2/sidebar';
import {getAccountName} from '../../../2_processes/role-sidebar/lib/account-name.ts';
import {AppSidebarProps} from '../model/props.ts';
import {ACTION_ITEMS, ITEMS} from '../const/items.tsx';

import ExitIcon from '../assets/exit.svg?react';

export function AppSidebar(props: AppSidebarProps) {
  return (
    <Sidebar
      selectedItemIndex={props.selectedItemIndex}
      items={ITEMS}
      actionItems={ACTION_ITEMS}
      logoutButtonProps={{
        icon: (
          <ExitIcon/>
        ),
        accountName: getAccountName(props.currentUser),
        onClick: () => {return;}
      }}/>
  );
}
