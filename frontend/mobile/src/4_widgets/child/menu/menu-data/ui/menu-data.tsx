import {View} from 'react-native';
import {createStyle} from '../consts/style';
import {TitleText} from '../../../../../7_shared/ui/text/title-text/title.text';
import {MiniCalendar} from '../../../../../7_shared/ui/special/mini-calendar';
import {setDataMenu} from '../../menu/model/menu-slice/menu-slice';
import {useAppDispatch} from '../../../../../../store/hooks';
import {MonthPicker} from '../../../../../7_shared/ui/special/mini-calendar/ui/month-picker';
import {useEffect, useState} from 'react';
import {DEFAULT_DATE} from '../../../../../7_shared/consts/default_date';
import {findFirstFullWeek} from '../../../../../7_shared/ui/special/mini-calendar/lib/dates-utils';
import {dateToISOWithoutTime} from '../../../../../7_shared/lib/date';

export function MenuData() {
  const styles = createStyle();
  const dispatch = useAppDispatch();

  const [selectedDate, setSelectedDate] = useState<Date>(DEFAULT_DATE);
  const [monthDate, setMonthDate] = useState<Date>(DEFAULT_DATE);

  useEffect(() => {
    dispatch(setDataMenu(dateToISOWithoutTime(selectedDate)));
  }, [selectedDate]);

  const handleDate = (date: Date) => {
    setMonthDate(date);
    setSelectedDate(date);
  };

  const handleMonth = (date: Date) => {
    setMonthDate(date);
    setSelectedDate(findFirstFullWeek(date));
  };

  return (
    <View style={styles.container}>
      <View style={styles.menuTitle}>
        <TitleText title={'Меню'}
          paddingBottom={0}/>
        <MonthPicker date={monthDate} onMonthChange={handleMonth}/>
      </View>
      <MiniCalendar selectionColor={'#E9632C'}
        currentDate={selectedDate}
        onDateChange={handleDate}/>
    </View>
  );
}
