import {NewDateButtonProps} from '../types/props';
import {Text, TouchableOpacity, View} from 'react-native';
import {useEffect, useState} from 'react';
import {getShortDayName} from '../lib/dates';
import {createNewDateButtonStyles} from '../consts/styles';
import {standartStyleMapper} from '../lib/date-style-mapper';
import {StandardDateProperties} from '../types/date-properties';

export function NewDateButton(props: NewDateButtonProps) {
  const [date, setDate] = useState(props.date);

  const mapStyles = () => standartStyleMapper(props as StandardDateProperties);

  const styles = createNewDateButtonStyles();
  const [currentStyle, setCurrentStyle]
    = useState(mapStyles());

  useEffect(() => {
    setCurrentStyle(mapStyles());
  }, [props.selected, props.cancelled, props.default]);

  useEffect(() => {
    setDate(props.date);
  }, [props.date]);

  const onPress = () => {
    props?.onPress?.();
  };

  return (
    <TouchableOpacity
      onPress={onPress}>
      <View
        style={styles[currentStyle]?.container}>

        <Text
          style={styles[currentStyle]?.dayNumber}>
          {date.getDate()}
        </Text>

        <Text
          style={styles[currentStyle]?.dayName}>
          {getShortDayName(date)}
        </Text>

      </View>
    </TouchableOpacity>
  );
}

