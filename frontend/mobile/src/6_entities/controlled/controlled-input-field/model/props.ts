import {InputFieldProps} from '../../../../7_shared/ui/fields/input-field';
import {Control, FieldErrors} from 'react-hook-form';

export type ControlledInputFieldProps<FormData> = {
  control: Control<any, any>,
  errors: FieldErrors,
} & InputFieldProps<FormData>
