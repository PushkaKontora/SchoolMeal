import {Text, View} from 'react-native';
import {ButtonIconed} from '../../../buttons/button-iconed';
import {monthPicker} from '../consts/styles';
import {MonthPickerProps} from '../types/props';
import {useEffect, useState} from 'react';
import {changeMonth, createDateFromMonthIndex, findNextMonth, findPrevMonth, getMonthName} from '../lib/month-utils';

export function MonthPicker(props: MonthPickerProps) {
  const [monthObject, setMonthObject] = useState(createDateFromMonthIndex(props.date));

  const onPrevButtonClick = () => {
    const month = findPrevMonth(monthObject);
    props.onMonthChange(month);
  };

  const onNextButtonClick = () => {
    const month = findNextMonth(monthObject);
    props.onMonthChange(month);
  };

  useEffect(() => {
    setMonthObject(createDateFromMonthIndex(props.date));
  }, [props.date]);

  return (
    <View
      style={monthPicker.container}>
      <ButtonIconed
        size={14}
        onPress={onPrevButtonClick}
        resource={require('../../../../../../assets/arrow-small-black-left.png')}/>

      <Text
        style={monthPicker.monthName}>
        {getMonthName(monthObject.getMonth())}
      </Text>

      <ButtonIconed
        size={14}
        onPress={onNextButtonClick}
        resource={require('../../../../../../assets/arrow-small-black-right.png')}/>
    </View>
  );
}
