import {DefaultInputProps} from './props.ts';
import {TabSelector} from '../../../../7_shared/ui/v2/interactive/tab-selector';
import {Container, TabSelectorContainer} from './styles.ts';

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
    </Container>
  );
}
