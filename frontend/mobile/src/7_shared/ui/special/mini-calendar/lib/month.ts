import {MONTHS} from '../config/config';
import {findMondayOnWeek} from './dates';

export function getMonthName(monthIndex: number) {
  return MONTHS[monthIndex];
}

export function createDateFromMonthIndex(date: Date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

export function getMonthOfLastDateInSlice(startOfSlice: Date, dayNumber: number) {
  const endOfSlice = new Date(startOfSlice);
  endOfSlice.setDate(endOfSlice.getDate() + dayNumber - 1);

  endOfSlice.setDate(1);
  return endOfSlice;
}

/**
 * @param directionFunc
 * @param currentMonth
 * @return Date[] Date с днем начала недели, Date типа (1, m, y): m - новый месяц, y - год, как в currentMonth]
 */
export function changeMonth(directionFunc: typeof findNextMonth, currentMonth: Date) {
  const firstDate = directionFunc(currentMonth);
  const mondayOnWeek = findMondayOnWeek(firstDate);
  const month = getMonthOfLastDateInSlice(mondayOnWeek, 7);

  return [mondayOnWeek, month];
}

export function findNextMonth(currentMonth: Date) {
  currentMonth.setMonth(currentMonth.getMonth() + 1);
  return currentMonth;
}

export function findPrevMonth(currentMonth: Date) {
  currentMonth.setMonth(currentMonth.getMonth() - 1);
  return currentMonth;
}