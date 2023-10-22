import {InputData} from '../../7_shared/ui/fields/input-field';
import {idChildData} from './types';

export const INPUT_DATA: InputData<idChildData> = {
  name: 'childId',
  label: 'id',
  type: '',
  options: {
    required: 'Вы не заполнили это поле'
  },
  placeholder: ''
};