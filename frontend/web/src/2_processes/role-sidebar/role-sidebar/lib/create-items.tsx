
import {ITEM_ROUTES, ITEMS} from '../const/items.tsx';
import {Role} from '../../../../5_features/auth';

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
