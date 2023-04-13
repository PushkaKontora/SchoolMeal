import {RefObject} from 'react';
import {InputField} from './input-field';

export type InputStyle = {
  width?: string,
  paddingVertical?: number,
  paddingHorizontal?: number,
  backgroundColor?: string,
  placeHolderColor?: string,
  color?: string
};

export type InputData = {
  options: any,
  label: string,
  name: string,
  type?: string,
  placeholder?: string,
  defaultValue?: string
};

export type InputFieldProps = {
  style?: InputStyle,
  data: InputData,
  errors: any,
  register?: any,
  onChangeText?: any,
  value?: any,
  inputRef?: RefObject<typeof InputField>
};
