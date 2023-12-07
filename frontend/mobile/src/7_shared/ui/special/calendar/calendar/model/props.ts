import {ComponentProps} from 'react';
import {Calendar as ExternalCalendar} from 'react-native-calendars';

export type CalendarProps = {

};

export type CalendarHeaderProps = {

};

export type PeriodDateBadgeProps = {

};

export type DayComponentProps = ComponentProps<NonNullable<ComponentProps<typeof ExternalCalendar>['dayComponent']>>;
