import {View} from 'react-native';
import {datePicker, monthPicker, styles} from './styles';
import {MiniCalendarProps} from './props';
import {useState} from 'react';
import {DEFAULT_DATE, DEFAULT_ITEM_NUMBER} from './config';
import {findDatesFrom} from './utils';
import {ButtonIconed} from '../../buttons/button-iconed';
import {DateButton} from './date-button';

export function MiniCalendar(props: MiniCalendarProps) {
  const [itemNumber, setItemNumber] = useState(props.itemNumber || DEFAULT_ITEM_NUMBER);

  const [dates, setDates] = useState(
    findDatesFrom(props.currentDate || DEFAULT_DATE(), itemNumber));

  return (
    <View
      style={styles.container}>

      <View
        style={monthPicker.container}>



      </View>

      <View
        style={datePicker.container}>

        <ButtonIconed
          size={20}
          onPress={() => {return;}}
          resource={require('../../../../../assets/arrow-big-gray-left.svg')}/>

        {
          dates.map((item, idx) =>
            <DateButton key={idx}
              date={item}
              selectionColor={props.selectionColor}
              onPress={() => {return;}}/>)
        }

        <ButtonIconed
          size={20}
          onPress={() => {return;}}
          resource={require('../../../../../assets/arrow-big-gray-right.svg')}/>

      </View>

    </View>
  );
}
