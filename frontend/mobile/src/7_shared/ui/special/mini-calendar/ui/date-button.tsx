import {DateButtonProps} from '../types/props';
import {Text, TouchableOpacity, View} from 'react-native';
import {useEffect, useState} from 'react';
import {getShortDayName} from '../lib/dates';
import {createContainerStyle, createTextStyle} from '../button-style-utils';

export function DateButton(props: DateButtonProps) {
  const [date, setDate] = useState(props.date);
  const [checked, setChecked] = useState(props?.checked || false);

  const [containerStyle, setContainerStyle] =
    useState(createContainerStyle(props.selectionColor, props?.checked || false));

  const [textStyle, setTextStyle] =
    useState(createTextStyle(props.selectionColor, props?.checked || false));

  useEffect(() => {
    setContainerStyle(createContainerStyle(props.selectionColor, checked));
    setTextStyle(createTextStyle(props.selectionColor, checked));
  }, [checked]);

  useEffect(() => {
    setChecked(props.checked || false);
  }, [props.checked]);

  useEffect(() => {
    setDate(props.date);
  }, [props.date]);

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
