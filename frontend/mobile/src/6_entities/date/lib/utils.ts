import {STRINGS} from '../consts/consts';
import {OPTIONS} from '../config/config';

export function formatDate(d: Date) {
  const formattedDate = d.toLocaleDateString('ru-RU', OPTIONS);
  const endPosition = formattedDate.length - 3;
  return formattedDate.slice(0, endPosition) + ' ' + STRINGS.ru.year;
}
