import {CancelledPeriodOut} from '../backend-types/nutrition/cancelled-period.ts';
import {CancelledPeriod} from '../frontend-types/nutrition/cancelled-period.ts';

export const toPeriod = (period: CancelledPeriodOut): CancelledPeriod => ({
  start: new Date(period.start),
  end: new Date(period.end)
});

export const toPeriodArray = (periods: CancelledPeriodOut[]) => periods.map(toPeriod);
