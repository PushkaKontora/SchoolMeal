import {ITEM_ROUTES, ITEMS} from '../const/items.tsx';
import {Role} from '../../../../5_features/auth';
import {ACTION_ITEMS} from '../const/action-items.tsx';
import {SidebarIconedButtonProps} from '../../../../7_shared/ui/v2/sidebar/components/iconed-button/props.ts';

export function createItems(onClick: (index: number) => void, navigate: (route: string) => unknown, role?: Role) {
  if (!role) {
    return [];
  }

  let result = ITEMS[role];
  const routes = ITEM_ROUTES[role];

  result = result.map((item, index) => ({
    ...item,
    onClick: () => {
      navigate(routes[index]);
      onClick(index);
    }
  }));

  return result;
}

export function createActionItems(role?: Role, clickCallbacks?: SidebarIconedButtonProps['onClick'][]) {
  if (!role) {
    return [];
  }

  if (role === Role.teacher) {
    return ACTION_ITEMS.map((item, index) => ({
      ...item,
      onClick: clickCallbacks?.[index]
    }));
  } else {
    return [];
  }
}
