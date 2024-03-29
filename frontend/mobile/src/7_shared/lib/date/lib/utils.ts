import {STRINGS} from '../consts/consts';
import {CASUAL_OPTIONS} from '../config/config';
import moment from 'moment-timezone';

export function formatDateToCasual(d: Date) {
  const formattedDate = d.toLocaleDateString('ru-RU', CASUAL_OPTIONS);
  const endPosition = formattedDate.length - 3;
  return formattedDate.slice(0, endPosition) + ' ' + STRINGS.ru.year;
}

export function dateToISOWithoutTime(d: Date): string {
  return [
    d.getFullYear(),
    (d.getMonth()+1).toString().padStart(2, '0'),
    d.getDate().toString().padStart(2, '0')
  ].join('-');
}

export function equalsDates(d1: Date, d2: Date) {
  return d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate();
}

export function isTodayDate(d: Date, tz: string) {
  const today = moment().tz(tz);
  return d.getFullYear() === today.year() &&
    d.getMonth() === today.month() &&
    d.getDate() === today.date();
}

export function isTomorrowDate(d: Date, tz: string) {
  const today = moment().tz(tz);
  const tomorrow = moment(today);
  tomorrow.add(1, 'days');
  return d.getFullYear() === tomorrow.year() &&
    d.getMonth() === tomorrow.month() &&
    d.getDate() === tomorrow.date();
}
