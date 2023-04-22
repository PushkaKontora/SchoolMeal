import {StyleSheet, Text, TouchableOpacity} from 'react-native';
import {ButtonPrimaryProps} from './props';
import {useEffect, useState} from 'react';
import {createStyle} from './style';

export function ButtonPrimary(props: ButtonPrimaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  useEffect(() => {
    setDisabled(Boolean(props.disabled));
  }, [props.disabled]);

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
