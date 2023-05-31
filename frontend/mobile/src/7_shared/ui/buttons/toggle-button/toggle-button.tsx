import {ToggleButtonProps} from './props';
import {Text, TouchableNativeFeedback, TouchableWithoutFeedback, View} from 'react-native';
import {styles} from './styles';
import {useEffect, useState} from 'react';

export function ToggleButton(props: ToggleButtonProps) {
  const [toggledRight, setToggledRight] = useState(props?.defaultState);

  useEffect(() => {
    setToggledRight(props.defaultState);
  }, [props.defaultState]);

  const onPress = (state: boolean) => {
    setToggledRight(state);
    props.onToggle(state);
  };

  return (
    <View style={styles.background}>
      <TouchableWithoutFeedback
        onPress={() => onPress(false)}>
        <View
          style={!toggledRight ? styles.active : styles.inactive}>
          <Text
            style={!toggledRight ? styles.activeText : styles.inactiveText}>
            {props.leftTitle}
          </Text>
        </View>
      </TouchableWithoutFeedback>
      <TouchableNativeFeedback
        onPress={() => onPress(true)}>
        <View
          style={toggledRight ? styles.active : styles.inactive}>
          <Text
            style={toggledRight ? styles.activeText : styles.inactiveText}>
            {props.rightTitle}
          </Text>
        </View>
      </TouchableNativeFeedback>
    </View>
  );
}
