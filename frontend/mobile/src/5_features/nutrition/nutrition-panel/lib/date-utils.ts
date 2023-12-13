import {isTodayDate} from '../../../../7_shared/lib/date/lib/utils';

export function isDateExpired(d: Date) {
  const expDate = setHoursTillAbleToCancel();

  if (isTodayDate(d)) {
    const now = new Date(Date.now());
    return now.valueOf() >= expDate.valueOf();
  }

  return d.valueOf() < expDate.valueOf();
}

export function setHoursTillAbleToCancel() {
  const now = new Date(Date.now());
  now.setHours(10, 0, 0, 0);
  return now;
}
