import {STRINGS} from '../consts/consts';
import {CASUAL_OPTIONS} from '../config/config';

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