import {DatePickerProps} from './props.ts';
import {ArrowButton, Container, DateTitle} from './styles.ts';

import {formatDate, getNextDate, getPreviousDate} from './lib.ts';

import ChevronLeft from './assets/chevron-left.svg?react';
import ChevronRight from './assets/chevron-right.svg?react';

export function DatePicker(props: DatePickerProps) {
  return (
    <Container $width={props.styles?.width}>
      <ArrowButton
        onClick={() => props.onDateChange(getPreviousDate(props.currentDate))}>
        <ChevronLeft/>
      </ArrowButton>
      <DateTitle>
        {formatDate(props.currentDate)}
      </DateTitle>
      <ArrowButton
        onClick={() => props.onDateChange(getNextDate(props.currentDate))}>
        <ChevronRight/>
      </ArrowButton>
    </Container>
  );
}
