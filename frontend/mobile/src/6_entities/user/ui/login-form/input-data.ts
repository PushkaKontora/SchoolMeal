import {InputData} from '../../../../7_shared/ui/fields/input-field';
import {LoginFormData} from './types';

export const INPUT_DATA: InputData<LoginFormData>[] = [
  {
    name: 'login',
    label: 'Логин',
    type: 'telephoneNumber',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: '+7 (000) 000-00-00'
  },
  {
    name: 'password',
    label: 'Пароль',
    type: 'password',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Пароль'
  }
];
