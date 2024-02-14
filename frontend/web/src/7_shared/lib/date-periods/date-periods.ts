export function isDateInPeriod(date: string | Date, startingDate: string | Date, endingDate: string | Date) {
  return date >= startingDate && date <= endingDate;
}

export function isDateInAnyPeriods(date: string | Date, periods: [string, string][]) {
  for (const p of periods) {
    if (isDateInPeriod(date, p[0], p[1])) {
      return true;
    }
  }

  return false;
}
