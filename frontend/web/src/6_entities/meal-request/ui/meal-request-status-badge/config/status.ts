import {StatusValue} from '../model/types.ts';
import {MealRequestStatus} from '../../../../../7_shared/model/meal-request-status.ts';

export const StatusValues: StatusValue<MealRequestStatus> = {
  [MealRequestStatus.NotApplied]: {
    name: 'Заявка не подана',
    color: '#E9632C'
  },
  [MealRequestStatus.Edit]: {
    name: 'Заявка на редактировании',
    color: '#FFDB20'
  },
  [MealRequestStatus.Applied]: {
    name: 'Заявка подана',
    color: '#2FCB8F'
  },
};
