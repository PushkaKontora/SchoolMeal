import {StatusValue} from '../model/types.ts';
import {MealApplicationFormStatus} from '../../../model/meal-application-form-status.ts';

export const StatusValues: StatusValue<MealApplicationFormStatus> = {
  [MealApplicationFormStatus.NotApplied]: {
    name: 'Заявка не подана',
    color: '#E9632C'
  },
  [MealApplicationFormStatus.Edit]: {
    name: 'Заявка на редактировании',
    color: '#FFDB20'
  },
  [MealApplicationFormStatus.Applied]: {
    name: 'Заявка подана',
    color: '#2FCB8F'
  },
};
