import {CalendarProps} from '../model/props';
import {Calendar as ExternalCalendar, DateData} from 'react-native-calendars';
import {Text} from 'react-native';
import {useEffect, useState} from 'react';
import {DayComponent} from './day-component';
import {generatePeriod} from '../lib/period';
import {dateToISOWithoutTime} from '../../../../../lib/date';
import {DEFAULT_DATE} from '../config/calendar-config';

export function Calendar(props: CalendarProps) {
  const initPeriod = () => {
    return generatePeriod(
      dateToISOWithoutTime(props.initialDate || DEFAULT_DATE()),
      dateToISOWithoutTime(props.initialDate || DEFAULT_DATE()));
  };

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
      const isSelectedDateLess = selectedDate < clickedDate;
      const leftDate = isSelectedDateLess ? selectedDate : clickedDate;
      const rightDate = isSelectedDateLess ? clickedDate : selectedDate;
      setMarkedDates(generatePeriod(leftDate, rightDate));
      setSelectPeriod(false);
    } else {
      setMarkedDates(generatePeriod(date.dateString, date.dateString));
      setSelectPeriod(true);
    }
  };

  return (
    <ExternalCalendar
      initialDate={dateToISOWithoutTime(props.initialDate || DEFAULT_DATE())}
      markingType={'period'}
      hideArrows={true}
      hideExtraDays={true}
      firstDay={1}
      markedDates={markedDates}
      onDayPress={onDayPress}
      dayComponent={(props) => (
        <DayComponent {...props}/>
      )}
      renderHeader={(date: any) => (
        <Text>
          {'Custom Header'}
        </Text>
      )}
    />
  );
}
