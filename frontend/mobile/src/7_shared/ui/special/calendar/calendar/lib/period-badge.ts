import {PERIOD_DATE_OPTIONS} from '../config/period-badge-config';

export function transformDateToString(date: Date) {
  return date.toLocaleDateString('ru-RU', PERIOD_DATE_OPTIONS);
}
