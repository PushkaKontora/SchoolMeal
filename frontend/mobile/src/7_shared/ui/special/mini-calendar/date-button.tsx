import {DateButtonProps} from './props';
import {Text, TouchableOpacity, View} from 'react-native';
import {dateButton} from './styles';
import {useEffect, useState} from 'react';
import {getShortDayName} from './utils';
import {createContainerStyle, createTextStyle} from './button-style-utils';

export function DateButton(props: DateButtonProps) {
  const [date, setDate] = useState(props.date);
  const [checked, setChecked] = useState(props?.checked as boolean);

  const [containerStyle, setContainerStyle] =
    useState(createContainerStyle(props.selectionColor, props?.checked as boolean));

  const [textStyle, setTextStyle] =
    useState(createTextStyle(props.selectionColor, props?.checked as boolean));

  useEffect(() => {
    setContainerStyle(createContainerStyle(props.selectionColor, checked));
    setTextStyle(createTextStyle(props.selectionColor, checked));
  }, [checked]);

  useEffect(() => {
    setChecked(props.checked as boolean);
  }, [props.checked]);

  const onPress = () => {
    setChecked(true);
    props.onPress();
  };

  return (
    <TouchableOpacity
      onPress={onPress}>
      <View
        style={containerStyle}>

        <Text
          style={textStyle}>
          {date.getDate()}
        </Text>

        <Text
          style={textStyle}>
          {getShortDayName(date)}
        </Text>

      </View>
    </TouchableOpacity>
  );
}
