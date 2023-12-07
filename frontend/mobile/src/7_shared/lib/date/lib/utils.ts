import {STRINGS} from '../consts/consts';
import {OPTIONS} from '../config/config';

export function formatDate(d: Date) {
  const formattedDate = d.toLocaleDateString('ru-RU', OPTIONS);
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
