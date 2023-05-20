import {ToggleButtonProps} from './props';
import {Text, TouchableNativeFeedback, TouchableWithoutFeedback, View} from 'react-native';
import {styles} from './styles';
import {useState} from 'react';

export function ToggleButton(props: ToggleButtonProps) {
  const [turnedOn, setTurnedOn] = useState(props?.defaultState);

  const onPress = (state: boolean) => {
    setTurnedOn(state);
    props.onToggle(state);
  };

  return (
    <View style={styles.background}>
      <TouchableWithoutFeedback
        onPress={() => onPress(false)}>
        <View
          style={!turnedOn ? styles.active : styles.inactive}>
          <Text
            style={!turnedOn ? styles.activeText : styles.inactiveText}>
            {props.turnedOffTitle}
          </Text>
        </View>
      </TouchableWithoutFeedback>
      <TouchableNativeFeedback
        onPress={() => onPress(true)}>
        <View
          style={turnedOn ? styles.active : styles.inactive}>
          <Text
            style={turnedOn ? styles.activeText : styles.inactiveText}>
            {props.turnedOnTitle}
          </Text>
        </View>
      </TouchableNativeFeedback>
    </View>
  );
}
