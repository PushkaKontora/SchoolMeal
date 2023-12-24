import {InputData} from '../../../7_shared/ui/fields/input-field';
import {CommentFormData} from '../model/comment-form-data';

export const INPUT_DATA: InputData<CommentFormData>[] = [
  {
    name: 'reason',
    label: 'Комментарий',
    type: 'text',
    options: {
      required: 'Это поле обязательно'
    },
    placeholder: 'Введите текст...'
  }
];
