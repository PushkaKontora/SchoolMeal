import {InputData} from '../../../7_shared/ui/fields/input-field';
import {AddChildData} from '../types';

export const INPUT_DATA: InputData<AddChildData> = {
  name: 'childId',
  label: 'id',
  type: '',
  options: {
    required: 'Вы не заполнили это поле'
  },
  placeholder: ''
};