import {MarkedDates} from 'react-native-calendars/src/types';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export function generatePeriod(startingDate: string, endingDate: string) {
  const result: MarkedDates = {};

  const date = new Date(startingDate);
  const endingDateObject = new Date(endingDate);
  let isoDate = dateToISOWithoutTime(date);

  while (date <= endingDateObject) {
    result[isoDate] = {
      startingDay: false,
      endingDay: false
    };

    date.setDate(date.getDate() + 1);
    isoDate = dateToISOWithoutTime(date);
  }

  result[startingDate].startingDay = true;
  result[endingDate].endingDay = true;

  return result;
}