import {DatePickerProps} from './props.ts';
import {ArrowButton, Container, DateTitle} from './styles.ts';

import {ChevronLeft} from './icons/date-picker-chevron-left.svg';

export function DatePicker(props: DatePickerProps) {
  return (
    <Container $width={props.styles?.width}>
      <ArrowButton>
        <ChevronLeft/>
      </ArrowButton>
      <DateTitle>

      </DateTitle>
      <ArrowButton>

      </ArrowButton>
    </Container>
  );
}
