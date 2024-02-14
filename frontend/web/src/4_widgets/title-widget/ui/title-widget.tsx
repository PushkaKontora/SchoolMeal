import {Container, Subtitle, Title} from './styles.ts';
import {TitleWidgetProps} from '../model/props.ts';

export function TitleWidget(props: TitleWidgetProps) {
  return (
    <Container>
      <Title>
        {props.title}
      </Title>
      {
        props.subtitle && (
          <Subtitle>
            {props.subtitle}
          </Subtitle>
        )
      }
    </Container>
  );
}
