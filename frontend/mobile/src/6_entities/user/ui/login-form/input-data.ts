import {InputData} from '../../../../7_shared/ui/fields/input-field';

export const INPUT_DATA: InputData[] = [
  {
    name: 'phone',
    label: 'Логин',
    type: 'telephoneNumber',
    options: {
      required: 'Вы не заполнили это поле'
    }
  },
  {
    name: 'password',
    label: 'Пароль',
    type: 'password',
    options: {
      required: 'Вы не заполнили это поле'
    }
  }
];
