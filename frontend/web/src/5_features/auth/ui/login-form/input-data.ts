import {InputData} from '../../../../7_shared/ui/fields/input-field';
import {LoginFormData} from './types';

export const INPUT_DATA: InputData<LoginFormData>[] = [
  {
    name: 'login',
    label: 'Логин',
    type: 'text',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Введите свой логин'
  },
  {
    name: 'password',
    label: 'Пароль',
    type: 'password',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Введите пароль'
  }
];
