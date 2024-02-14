import {CSSProperties} from 'react';

export type DatePickerStyles = {
  width: CSSProperties['width']
}

export type DatePickerProps = {
  currentDate: Date,
  onDateChange: (newDate: Date) => void,
  styles?: DatePickerStyles
}
