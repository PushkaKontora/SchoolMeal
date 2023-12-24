import {RU_LOCALE} from '../const/locales';

export function dateToHeaderString(d: Date) {
  const months = RU_LOCALE.monthNames;
  const monthName = months[d.getMonth()];

  return `${monthName} ${d.getFullYear()}`;
}
