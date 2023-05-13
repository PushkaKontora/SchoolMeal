import {InputData} from '../../../../7_shared/ui/fields/input-field';
import {SignUpFormData} from './types';

export const INPUT_DATA: InputData<SignUpFormData>[] = [
  {
    name: 'firstName',
    label: 'Имя',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Имя'
  },
  {
    name: 'lastName',
    label: 'Фамилия',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Фамилия'
  },
  {
    name: 'phone',
    label: 'Телефон',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: '+7 (000) 000-00-00'
  },
  {
    name: 'email',
    label: 'Адрес электронной почты',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Адрес электронной почты'
  },
  {
    name: 'password',
    label: 'Пароль',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Пароль'
  },
  {
    name: 'confirmPassword',
    label: 'Подтверждение пароля',
    type: '',
    options: {
      required: 'Вы не заполнили это поле'
    },
    placeholder: 'Подтверждение пароля'
  }
];