import {ControlledInputFieldProps} from '../../../controlled-input-field';

export type InputFieldLimitedProps<FormData> = {
  symbolLimit: number
} & ControlledInputFieldProps<FormData>;
