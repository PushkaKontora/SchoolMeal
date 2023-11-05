import {InputData} from '../../../7_shared/ui/fields/input-field';
import {LimitedFieldData} from '../types/limited-field-data';

export const INPUT_DATA: InputData<LimitedFieldData>[] = [
  {
    name: 'message',
    label: 'Отзыв',
    type: 'text',
    options: {
      required: 'Это поле обязательно'
    },
    placeholder: 'Введите текст...'
  }
];
