import {InputFieldProps} from './props.ts';
import {InputFieldContainer} from './styles.ts';
import {DEFAULT_PLACEHOLDER, DEFAULT_TYPE} from './config.ts';

export function InputField<FormData>(props: InputFieldProps<FormData>) {
  const data = props.data;

  return (
    <InputFieldContainer
      type={data.type || DEFAULT_TYPE}
      placeholder={data.placeholder || DEFAULT_PLACEHOLDER}

      defaultValue={data.defaultValue}
      onChange={props.onChangeText}
      value={props.value}
    />
  );
}
