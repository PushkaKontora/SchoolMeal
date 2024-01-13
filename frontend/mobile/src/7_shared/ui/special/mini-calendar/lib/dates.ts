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

export function isEqualDates(date1: Date, date2: Date) {
  return date1.getFullYear() == date2.getFullYear() &&
    date1.getMonth() == date2.getMonth() &&
    date1.getDate() == date2.getDate();
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

export function findMondayOnWeek(date: Date) {
  const result = new Date(date);
  const day = date.getDay();
  const dateShift = day == 0 ? -6 : - day + 1;
  result.setDate(result.getDate() + dateShift);

  return result;
}

export function findFirstFullWeek(month: Date) {
  const result = new Date(month);
  const day = month.getDay();
  let dateShift = 7 - day + 1;

  if (day == 1) {
    dateShift = 0;
  } else if (day == 0) {
    dateShift = 1;
  }

  result.setDate(month.getDate() + dateShift);

  return result;
}
