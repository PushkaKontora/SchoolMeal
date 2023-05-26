import {SHORT_WEEKDAYS} from '../config/config';

export function findDatesFrom(selectedDate: Date, amount: number): Date[] {
  const result = [selectedDate];

  for (let i = 1; i < amount; i++) {
    const nextDay = new Date(selectedDate);
    nextDay.setDate(nextDay.getDate() + i);
    result.push(nextDay);
  }

  return result;
}

export function getPreferredMonth(dates: Date[]) {
  const months: {[index: string]: number} = {};

  for (const date of dates) {
    const month = date.getMonth();
    months[month] = months[month] || 0;

    months[month] += 1;
  }

  const preferredMonth = Object
    .entries(months)
    .reduce((prev, curr) => {
      return prev[1] > curr[1] ? prev : curr;
    })[0];
  return preferredMonth;
}

export function findNext(currentLeftDate: Date, amount: number) {
  const date = currentLeftDate.getDate();
  const newLeftDate = new Date(currentLeftDate);
  newLeftDate.setDate(date + amount);

  return findDatesFrom(newLeftDate, amount);
}

export function findPrev(currentLeftDate: Date, amount: number) {
  const date = currentLeftDate.getDate();
  const newLeftDate = new Date(currentLeftDate);
  newLeftDate.setDate(date - amount);

  return findDatesFrom(newLeftDate, amount);
}

export function getShortDayName(date: Date) {
  return SHORT_WEEKDAYS[date.getDay()];
}
