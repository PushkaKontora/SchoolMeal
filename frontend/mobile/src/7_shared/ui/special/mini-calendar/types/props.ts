import {PaddingAreaProps} from '../../../styling/padding-area';

export type MiniCalendarProps = {
  selectionColor: string,
  currentDate?: Date,
  itemNumber?: number,
  onDateChange: (date: Date) => void,
  paddingProps?: PaddingAreaProps
};

export type DateButtonProps = {
  date: Date,
  checked?: boolean,
  selectionColor: string,
  onPress: () => void
}
