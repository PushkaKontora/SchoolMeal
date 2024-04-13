import {NotificationCardProps} from '../../model/props.ts';
import {Card, Description, Name, Reason} from './styles.ts';

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
      <Description>
        {props.body}
      </Description>
    </Card>
  );
}
