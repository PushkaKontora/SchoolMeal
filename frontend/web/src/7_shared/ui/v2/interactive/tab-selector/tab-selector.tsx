import {TabSelectorProps} from './props.ts';
import {Container, Tab} from './styles.ts';

export function TabSelector(props: TabSelectorProps) {
  return (
    <Container>
      {
        props.tabs.map((item, index) => (
          <Tab
            onClick={item.onClick}
            $selected={props.selected === index}>
            {item.name}
          </Tab>
        ))
      }
    </Container>
  );
}
