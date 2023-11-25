import {InputData} from '../../../../7_shared/ui/fields/input-field';
import {FeedbackFormData} from './feedback-form-data';

export const INPUT_DATA: InputData<FeedbackFormData>[] = [
  {
    name: 'text',
    label: 'Отзыв',
    type: 'text',
    options: {
      required: 'Это поле обязательно'
    },
    placeholder: 'Введите текст...'
  }
];
