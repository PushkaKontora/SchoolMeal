import {
  FormDataOptions,
  FormErrors,
  FormInputRef,
  FormOnChangeText,
  FormRegister
} from '../../../model/forms/form-types';

export type InputStyle = {
  width?: string,
  paddingVertical?: number,
  paddingHorizontal?: number,
  backgroundColor?: string,
  placeHolderColor?: string,
  borderRadius?: number,
  borderColor?: string,
  borderWidth?: number,
  color?: string
};

export type InputData<FormData> = {
  options: FormDataOptions,
  label: string,
  name: keyof FormData,
  type?: string,
  placeholder?: string,
  defaultValue?: string
};

export type InputFieldProps<FormData> = {
  style?: InputStyle,
  data: InputData<FormData>,
  errors: FormErrors,
  register?: FormRegister,
  onChangeText?: FormOnChangeText,
  onFocus?: () => void,
  onBlur?: () => void,
  value?: any,
  autoFocus?: boolean,
  inputRef?: FormInputRef,
  maxLength?: number,
  numberOfLines?: number
};
