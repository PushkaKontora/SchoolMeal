import {transformDateForReason} from './date-for-reason.ts';

export function createReason(startDate: Date, endDate?: Date) {
  return `не будет питаться ${transformDateForReason(startDate)} ${endDate ? transformDateForReason(endDate) : ''}`;
}
