import {DayComponentProps} from '../model/props';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export function selectDateTextStyles(props: DayComponentProps) {
  if (props.date) {
    if (props.date?.dateString <= dateToISOWithoutTime(props.passedDateUntil)) {
      return 'pastDateText';
    }
  }

  return 'dateText';
}
