import {SidebarIconedButtonProps} from '../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

import MyClassesIcon from '../assets/my_classes.svg?react';
import ApplyRequestIcon from '../assets/apply_request.svg?react';
import RequestHistoryIcon from '../assets/request_history.svg?react';

import NotificationIcon from '../assets/notifications.svg?react';

export const ITEMS: SidebarIconedButtonProps[] = [
  {
    icon: (
      <MyClassesIcon/>
    ),
    text: 'Мои классы',
    onClick: () => {return;}
  },
  {
    icon: (
      <ApplyRequestIcon/>
    ),
    text: 'Подать заявку',
    onClick: () => {return;},
    active: true
  },
  {
    icon: (
      <RequestHistoryIcon/>
    ),
    text: 'История заявок',
    onClick: () => {return;}
  }
];

export const ACTION_ITEMS: SidebarIconedButtonProps[] = [
  {
    icon: (
      <NotificationIcon/>
    ),
    text: 'Уведомления',
    onClick: () => {return;}
  }
];
