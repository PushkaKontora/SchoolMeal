import {PaddingAreaProps} from '../../../styling/padding-area';
import {StandardDateProperties} from './date-properties';

export type DateButtonProps = {
  date: Date,
  checked?: boolean,
  selectionColor: string,
  onPress: () => void
};

export type NewDateButtonProps = {
  date: Date,
  onPress?: () => void
} & StandardDateProperties;

export type DateInfo = {
  [index: string]: StandardDateProperties
};

export type MiniCalendarProps = {
  currentDate?: Date,
  itemNumber?: number,
  dateInfo?: DateInfo,
  onDateChange: (date: Date) => void,
  paddingProps?: PaddingAreaProps
};

export type MonthPickerProps = {
  date: Date,
  onMonthChange: (newDate: Date) => void
};
