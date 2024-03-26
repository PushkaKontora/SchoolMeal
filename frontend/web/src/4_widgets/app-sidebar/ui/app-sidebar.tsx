import {Sidebar} from '../../../7_shared/ui/v2/sidebar';
import {AppSidebarProps} from '../model/props.ts';

import ExitIcon from '../assets/exit.svg?react';
import {ACTION_ITEMS} from '../const/action-items.tsx';

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
        accountName: props.userName || '',
        onClick: () => {return;}
      }}/>
  );
}
