import {SwitchProps} from './props';
import {TouchableWithoutFeedback, View} from 'react-native';
import {useEffect, useState} from 'react';
import {createStyle} from './styles';

export function Switch(props: SwitchProps) {
  const [turnedOn, setTurnedOn] = useState(props?.defaultState as boolean);

  let styles = createStyle(turnedOn);

  const onPress = () => {
    const prevTurnedOn = turnedOn;
    setTurnedOn(!turnedOn);
    props.onToggle(prevTurnedOn);
  };

  useEffect(() => {
    styles = createStyle(turnedOn);
  }, [turnedOn]);

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
