import {Control, FieldErrors} from 'react-hook-form';
import {InputFieldProps} from '../input-field';

export type ControlledInputFieldProps<FormData> = {
  control: Control<any, any>,
  errors: FieldErrors
} & InputFieldProps<FormData>