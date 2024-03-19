import {Role} from '../../../../7_shared/model/role.ts';
import HomeIcon from '../assets/my_classes.svg?react';
import ApplyRequestIcon from '../assets/apply_request.svg?react';
import RequestHistoryIcon from '../assets/request_history.svg?react';
import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../../../3_pages/routing';
import {SidebarIconedButtonProps} from '../../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

export const ITEMS: {[role in Role]: SidebarIconedButtonProps[]} = {
  [Role.teacher]: [
    {
      icon: (
        <HomeIcon/>
      ),
      text: 'Мои классы'
    },
    {
      icon: (
        <ApplyRequestIcon/>
      ),
      text: 'Подать заявку'
    },
    {
      icon: (
        <RequestHistoryIcon/>
      ),
      text: 'История заявок'
    }
  ],
  [Role.canteen_staff]: [
    {
      icon: (
        <HomeIcon/>
      ),
      text: 'Заявки на питание'
    }
  ]
};

export const ITEM_ROUTES = {
  [Role.teacher]: [
    TEACHER_ROUTES.MyClasses,
    TEACHER_ROUTES.ApplyRequest,
    TEACHER_ROUTES.History
  ],
  [Role.canteen_staff]: [
    CANTEEN_STAFF_ROUTES.Requests
  ]
};