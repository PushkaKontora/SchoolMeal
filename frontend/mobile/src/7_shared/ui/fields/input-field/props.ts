import {RefObject} from 'react';
import {InputField} from './input-field';

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
  options: any,
  label: string,
  name: keyof FormData,
  type?: string,
  placeholder?: string,
  defaultValue?: string
};

export type InputFieldProps<FormData> = {
  style?: InputStyle,
  data: InputData<FormData>,
  errors: any,
  register?: any,
  onChangeText?: any,
  value?: any,
  inputRef?: RefObject<typeof InputField>
};
