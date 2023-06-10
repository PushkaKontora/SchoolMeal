import {View} from 'react-native';
import {datePicker, styles} from '../consts/styles';
import {MiniCalendarProps} from '../types/props';
import {useEffect, useState} from 'react';
import {DEFAULT_DATE, DEFAULT_ITEM_NUMBER} from '../config/config';
import {findDatesFrom, findNext, findPrev} from '../lib/dates-utils';
import {ButtonIconed} from '../../../buttons/button-iconed';
import {DateButton} from './date-button';
import {PaddingArea} from '../../../styling/padding-area';
import {DEFAULT_VERTICAL_PADDING} from '../consts/consts';

export function MiniCalendar(props: MiniCalendarProps) {
  // === states ===
  const [itemNumber, setItemNumber] = useState(props.itemNumber || DEFAULT_ITEM_NUMBER);

  const [dates, setDates] = useState<Date[]>(
    findDatesFrom(props.currentDate || DEFAULT_DATE(), itemNumber));

  const [checkedIndex, setCheckedIndex] = useState(0);

  // === functions ===

  const onDateButtonChange = (index: number) => {
    setCheckedIndex(index);
    props.onDateChange(dates[index]);
  };

  const onDatePickerLeftPress = () => {
    setDates(findPrev(dates[0], itemNumber));
  };

  const onDatePickerRightPress = () => {
    setDates(findNext(dates[0], itemNumber));
  };

  // === useEffects ===

  useEffect(() => {
    onDateButtonChange(0);
  }, [dates]);

  // === render ===
  return (
    <PaddingArea
      paddingVertical={DEFAULT_VERTICAL_PADDING}
      {...props?.paddingProps}>
      <View
        style={styles.container}>

        <View
          style={datePicker.container}>

          <ButtonIconed
            size={20}
            onPress={onDatePickerLeftPress}
            resource={require('../../../../../../assets/arrow-big-gray-left.png')}/>

          {
            dates.map((item, idx) =>
              <DateButton key={idx}
                checked={checkedIndex === idx}
                date={item}
                selectionColor={props.selectionColor}
                onPress={() => {
                  onDateButtonChange(idx);
                }}/>)
          }

          <ButtonIconed
            size={20}
            onPress={onDatePickerRightPress}
            resource={require('../../../../../../assets/arrow-big-gray-right.png')}/>

        </View>

      </View>
    </PaddingArea>
  );
}
