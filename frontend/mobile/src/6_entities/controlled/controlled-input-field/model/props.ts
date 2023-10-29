import {InputFieldProps} from '../../../../7_shared/ui/fields/input-field';
import {FormControl} from '../../../../7_shared/model/forms/form-types';

export type ControlledInputFieldProps<FormData> = {
  control: FormControl
} & InputFieldProps<FormData>
