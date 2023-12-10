import {ComponentProps} from 'react';
import {Calendar as ExternalCalendar} from 'react-native-calendars';

export type CalendarProps = {
  onPeriodChange: (startingDate: Date, endingDate: Date) => void
  initialDate?: Date
};

export type CalendarHeaderProps = {

};

export type PeriodDateBadgeProps = {
  startingDate: Date,
  endingDate?: Date,
  transformDateToString?: (d: Date) => string
};

export type DayComponentProps = ComponentProps<NonNullable<ComponentProps<typeof ExternalCalendar>['dayComponent']>>;
