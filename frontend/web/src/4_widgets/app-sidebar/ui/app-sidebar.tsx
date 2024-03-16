import {Sidebar} from '../../../7_shared/ui/v2/sidebar';
import {AppSidebarProps} from '../model/props.ts';

import ExitIcon from '../assets/exit.svg?react';
import {ACTION_ITEMS} from '../const/action-items.tsx';
import {getFullName} from '../../../6_entities/user';

export function AppSidebar(props: AppSidebarProps) {
  return (
    <Sidebar
      selectedItemIndex={props.selectedItemIndex}
      items={props.items}
      actionItems={ACTION_ITEMS}
      logoutButtonProps={{
        icon: (
          <ExitIcon/>
        ),
        accountName: getFullName(props.currentUser),
        onClick: () => {return;}
      }}/>
  );
}
