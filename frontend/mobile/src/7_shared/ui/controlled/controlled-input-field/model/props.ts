import {FormControl} from '../../../../model/forms/form-types';
import {InputFieldProps} from '../../../fields/input-field';

export type ControlledInputFieldProps<FormData> = {
  control: FormControl
} & InputFieldProps<FormData>
