import {CalendarProps} from '../model/props';
import {Calendar as ExternalCalendar, DateData} from 'react-native-calendars';
import {Text} from 'react-native';
import {useEffect, useState} from 'react';
import {DayComponent} from './day-component';
import {generatePeriod} from '../lib/lib';
import {LocaleConfig} from 'react-native-calendars/src';

export function Calendar(props: CalendarProps) {
  const [markedDates, setMarkedDates]
    = useState(generatePeriod('2023-11-17', '2023-11-17'));
  const [selectPeriod, setSelectPeriod] = useState(true);

  useEffect(() => {
    LocaleConfig.locales['ru'] = {
      monthNames: [
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'Mai',
        'Juin',
        'Juillet',
        'Août',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre'
      ],
      monthNamesShort: ['Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.'],
      dayNames: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
      today: "Aujourd'hui",
      dayNamesShort: ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
    };
    LocaleConfig.defaultLocale = 'ru';
  }, []);

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
      initialDate={'2023-11-01'}
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
