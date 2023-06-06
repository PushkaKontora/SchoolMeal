import {Text, View} from 'react-native';
import {ButtonIconed} from '../../../buttons/button-iconed';
import {monthPicker} from '../consts/styles';
import {MonthPickerProps} from '../types/props';
import {useEffect, useState} from 'react';
import {createDateFromMonthIndex, findNext, findPrev, getMonthName} from '../lib/month-utils';

export function MonthPicker(props: MonthPickerProps) {
  const [monthObject, setMonthObject] = useState(createDateFromMonthIndex(props.date));

  useEffect(() => {
    setMonthObject(createDateFromMonthIndex(props.date));
  }, [props.date]);

  const onPrevButtonClick = () => {
    setMonthObject(prev => {
      const newDate = findPrev(prev);
      props.onMonthChange(newDate);
      return newDate;
    });
  };

  const onNextButtonClick = () => {
    setMonthObject(prev => {
      const newDate = findNext(prev);
      props.onMonthChange(newDate);
      return newDate;
    });
  };

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
