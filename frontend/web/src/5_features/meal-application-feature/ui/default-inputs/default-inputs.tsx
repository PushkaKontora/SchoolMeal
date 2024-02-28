import {Container, DatePickerContainer, TabSelectorContainer} from './styles.ts';
import {TabSelector} from '../../../../7_shared/ui/v2/interactive/tab-selector';
import {DefaultInputProps} from './props.ts';
import {DatePicker} from '../../../../7_shared/ui/v2/interactive/date-picker/date-picker.tsx';

export function DefaultInputs(props: DefaultInputProps) {
  return (
    <Container>
      <TabSelectorContainer>
        <TabSelector
          selected={props.selectedClassIndex}
          tabs={props.classNames.map((item, index) => ({
            name: item,
            onClick: () => props.onClassSelect(index)
          }))}/>
      </TabSelectorContainer>
      <DatePickerContainer>
        <DatePicker
          currentDate={props.date}
          onDateChange={props.onDateSelect}/>
      </DatePickerContainer>
    </Container>
  );
}
