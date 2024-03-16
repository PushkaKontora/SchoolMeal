import {User} from '../../../../7_shared/model/user.ts';
import {ITEM_ROUTES, ITEMS} from '../const/items.tsx';

export function createItems(onClick: (index: number) => void, navigate: (route: string) => unknown, user?: User) {
  if (!user) {
    return [];
  }

  let result = ITEMS[user.role];
  const routes = ITEM_ROUTES[user.role];

  result = result.map((item, index) => ({
    ...item,
    onClick: () => {
      navigate(routes[index]);
      onClick(index);
    }
  }));

  return result;
}
