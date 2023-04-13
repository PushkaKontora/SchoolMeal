import {TextInput, View} from 'react-native';
import {InputFieldProps} from './props';
import {createStyle} from './style';
import {PLACEHOLDER_COLOR} from './consts';

export function InputField(props: InputFieldProps) {
  const styles = createStyle(props.style);
  const data = props.data;

  return (
    <View>
      <TextInput
        style={styles.default}
        placeholderTextColor={PLACEHOLDER_COLOR}

        textContentType={data.type}
        placeholder={data.placeholder}
        defaultValue={data.defaultValue}

        ref={props.inputRef}
        onChangeText={props.onChangeText}
        value={props.value}
      />
    </View>

  );
}
