import {DEFAULT_DATE_OPTIONS} from './config.ts';
import moment from 'moment-timezone';

export function formatDate(date: Date) {
  const result = date.toLocaleString('ru-RU', DEFAULT_DATE_OPTIONS);

  return result
    .replace(',', '')
    .replace('г.', '');
}

export function getPreviousDate(date: Date) {
  return moment(date).subtract(1, 'days').toDate();
}

export function getNextDate(date: Date) {
  return moment(date).add(1, 'days').toDate();
}
