export function isDateInPeriod(date: Date, startingDate: Date, endingDate: Date) {
  return date.getTime() >= startingDate.getTime() && date.getTime()  <= endingDate.getTime() ;
}

export function isDateInAnyPeriods(date: Date, periods: [Date, Date][]) {
  for (const p of periods) {
    if (isDateInPeriod(date, p[0], p[1])) {
      return true;
    }
  }

  return false;
}
