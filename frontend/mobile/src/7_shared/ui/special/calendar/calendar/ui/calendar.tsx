import {CalendarProps} from '../model/props';
import {Calendar as ExternalCalendar, DateData} from 'react-native-calendars';
import {useEffect, useState} from 'react';
import {DayComponent} from './day-component';
import {generatePeriod} from '../lib/period';
import {dateToISOWithoutTime} from '../../../../../lib/date';
import {DEFAULT_DATE} from '../config/calendar-config';
import {CalendarHeader} from './calendar-header';
import {TODAY_DATE} from '../config/day-config';

export function Calendar(props: CalendarProps) {
  const initPeriod = () => {
    return generatePeriod(
      dateToISOWithoutTime(props.initialDate || DEFAULT_DATE()),
      dateToISOWithoutTime(props.initialDate || DEFAULT_DATE()));
  };

  const [passedDatesUntil]
    = useState(props.passedDatesUntil || TODAY_DATE());
  const [month, setMonth]
    = useState(dateToISOWithoutTime(props.initialDate || DEFAULT_DATE()));
  const [markedDates, setMarkedDates]
    = useState(initPeriod());
  const [selectPeriod, setSelectPeriod] = useState(true);

  useEffect(() => {
    const dates = Object.keys(markedDates);
    const datesAmount = dates.length;

    props.onPeriodChange(new Date(dates[0]),
      new Date(dates[datesAmount - 1]));
  }, [markedDates]);

  const onDayPress = (date: DateData) => {
    if (selectPeriod) {
      const selectedDate = Object.keys(markedDates)[0];
      const clickedDate = date.dateString;
      setMarkedDates(generatePeriod(selectedDate, clickedDate));
    } else {
      setMarkedDates(generatePeriod(date.dateString, date.dateString));
    }
    setSelectPeriod(prevState => !prevState);
  };

  const onHeaderLeftPress = () => {
    const date = new Date(month);
    date.setMonth(date.getMonth() - 1);
    setMonth(dateToISOWithoutTime(date));
  };

  const onHeaderRightPress = () => {
    const date = new Date(month);
    date.setMonth(date.getMonth() + 1);
    setMonth(dateToISOWithoutTime(date));
  };

  return (
    <ExternalCalendar
      initialDate={month}
      markingType={'period'}
      hideArrows={true}
      hideExtraDays={true}
      firstDay={1}
      markedDates={markedDates}
      onDayPress={onDayPress}
      dayComponent={(props) => (
        <DayComponent
          {...props}
          passedDateUntil={passedDatesUntil}/>
      )}
      renderHeader={(date: Date) => (
        <CalendarHeader
          onLeftPress={onHeaderLeftPress}
          onRightPress={onHeaderRightPress}
          monthDate={date}/>
      )}
    />
  );
}
