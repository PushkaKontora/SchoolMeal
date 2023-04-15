import {ButtonSecondaryProps} from './props';
import {StyleSheet, Text, TouchableOpacity} from 'react-native';
import {useState} from 'react';
import {createStyle} from './style';

export function ButtonSecondary(props: ButtonSecondaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  const styles = createStyle(props);

  return (
    <TouchableOpacity
      disabled={disabled}
      onPress={props.onPress}
      style=
        {disabled ? StyleSheet.compose(styles.default, styles.disabled) :  styles.default}>
      <Text
        style={styles.title}>
        {props.title}
      </Text>
    </TouchableOpacity>
  );
}
