import {TODAY_DATE} from '../config/day-config';
import {DayComponentProps} from '../model/props';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export function selectDateTextStyles(props: DayComponentProps) {
  const today = TODAY_DATE();

  if (props.date) {
    if (props.date?.dateString < dateToISOWithoutTime(today)) {
      return 'pastDateText';
    }
  }

  return 'dateText';
}
