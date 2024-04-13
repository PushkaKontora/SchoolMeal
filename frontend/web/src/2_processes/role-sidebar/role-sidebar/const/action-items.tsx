import NotificationIcon from '../assets/notifications.svg?react';

import {SidebarIconedButtonProps} from '../../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

export const ACTION_ITEMS: SidebarIconedButtonProps[] = [
  {
    icon: (
      <NotificationIcon/>
    ),
    text: 'Уведомления'
  }
];
