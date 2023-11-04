import {TextInput} from 'react-native';
import {InputFieldProps} from './props';
import {createStyle} from './style';
import {PLACEHOLDER_COLOR} from './consts';

export function InputField<FormData>(props: InputFieldProps<FormData>) {
  const styles = createStyle(props.style);
  const data = props.data;

  return (
    <TextInput
      style={styles.default}
      placeholderTextColor={props.style?.placeHolderColor || PLACEHOLDER_COLOR}
      secureTextEntry={data?.type === 'password'}

      placeholder={data.placeholder || ''}
      defaultValue={data.defaultValue}

      onChangeText={props.onChangeText}
      onFocus={props.onFocus}
      onBlur={props.onBlur}
      value={props.value}
      ref={props.inputRef}
      autoFocus={props.autoFocus}
      maxLength={props.maxLength}
      numberOfLines={props.numberOfLines}
    />
  );
}
