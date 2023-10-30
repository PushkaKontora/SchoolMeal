import {TextInput, View} from 'react-native';
import {TextFormProps} from './props';
import {createStyle} from './style';

export function TextForm(props: TextFormProps) {
  const styles = createStyle();

  return (
    <View>
      <TextInput style={styles.input}
        onChangeText={props.functionChangeText}></TextInput>
    </View>
  );
}
