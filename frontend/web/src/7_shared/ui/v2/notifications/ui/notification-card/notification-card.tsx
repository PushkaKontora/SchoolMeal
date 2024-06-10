import {NotificationCardProps} from '../../model/props.ts';
import {Card, Description, Mark, Name, Reason} from './styles.ts';

export function NotificationCard(props: NotificationCardProps) {
  return (
    <Card
      $read={props.read}>
      <Name>
        {props.title}
      </Name>
      <Reason>
        {props.subtitle}
      </Reason>
      <Mark>
        {props.mark}
      </Mark>
      {
        props.body && (
          <Description>
            {props.body}
          </Description>
        )
      }
    </Card>
  );
}
