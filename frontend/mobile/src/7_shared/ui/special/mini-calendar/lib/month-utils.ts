import {MONTHS} from '../config/config';

export function getMonthName(monthIndex: number) {
  return MONTHS[monthIndex];
}

export function createDateFromMonthIndex(date: Date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

export function findNext(currentMonth: Date) {
  currentMonth.setMonth(currentMonth.getMonth() + 1);
  return currentMonth;
}

export function findPrev(currentMonth: Date) {
  currentMonth.setMonth(currentMonth.getMonth() - 1);
  return currentMonth;
}