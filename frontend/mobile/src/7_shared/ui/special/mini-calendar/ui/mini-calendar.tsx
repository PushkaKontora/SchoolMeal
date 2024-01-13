import {View} from 'react-native';
import {datePicker, styles} from '../consts/styles';
import {MiniCalendarProps} from '../types/props';
import {useEffect, useRef, useState} from 'react';
import {DEFAULT_DATE, DEFAULT_ITEM_NUMBER} from '../config/config';
import {findDatesFrom, findNext, findPrev, isEqualDates} from '../lib/dates';
import {ButtonIconed} from '../../../buttons/button-iconed';
import {PaddingArea} from '../../../styling/padding-area';
import {DEFAULT_VERTICAL_PADDING} from '../consts/consts';
import {NewDateButton} from './new-date-button';
import {dateToISOWithoutTime} from '../../../../lib/date';

export function MiniCalendar(props: MiniCalendarProps) {
  // === states ===
  const [itemNumber] = useState(props.itemNumber || DEFAULT_ITEM_NUMBER);

  const [dates, setDates] = useState<Date[]>(
    findDatesFrom(props.currentDate || DEFAULT_DATE(), itemNumber));

  //const [checkedIndex, setCheckedIndex] = useState(0);
  const checkedIndexRef = useRef(0);

  // === callbacks ===

  const onDateButtonChange = (index: number) => {
    //setCheckedIndex(index);
    checkedIndexRef.current = index;
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

  useEffect(() => {
    if (props.currentDate) {
      if (!isEqualDates(props.currentDate, dates[checkedIndexRef.current])) {
        setDates(findDatesFrom(props.currentDate, itemNumber));
      }
    }
  }, [props.currentDate]);

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
            resource={require('../../../../../../assets/arrow-small-black-left.png')}/>

          {
            dates.map((item, idx) =>
              <NewDateButton
                key={idx}
                date={item}
                selected={checkedIndexRef.current === idx}
                {...props?.dateInfo?.[dateToISOWithoutTime(item)]}
                onPress={() => {
                  onDateButtonChange(idx);
                }}/>)
          }

          <ButtonIconed
            size={20}
            onPress={onDatePickerRightPress}
            resource={require('../../../../../../assets/arrow-small-black-right.png')}/>

        </View>

      </View>
    </PaddingArea>
  );
}
