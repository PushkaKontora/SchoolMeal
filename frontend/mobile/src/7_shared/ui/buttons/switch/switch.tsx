import {SwitchProps} from './props';
import {TouchableWithoutFeedback, View} from 'react-native';
import {useEffect, useState} from 'react';
import {createStyle} from './styles';

export function Switch(props: SwitchProps) {
  const [turnedOn, setTurnedOn] = useState(props?.defaultState || false);

  let styles = createStyle(turnedOn);

  useEffect(() => {
    styles = createStyle(turnedOn);
  }, [turnedOn]);

  useEffect(() => {
    setTurnedOn(props.defaultState || false);
  }, [props.defaultState]);

  const onPress = () => {
    setTurnedOn((prev) => {
      props.onToggle(!prev);
      return !prev;
    });
  };

  return (
    <TouchableWithoutFeedback
      onPress={onPress}>
      <View
        style={styles.background}>
        <View style={styles.pin}></View>
      </View>
    </TouchableWithoutFeedback>
  );
}
