import {MealRequestStatusBadgeProps} from '../model/props.ts';
import {Container, Status, Title} from '../styles/styles.ts';
import {useEffect, useState} from 'react';
import {StatusValues} from '../config/status.ts';

export function MealRequestStatusBadge(props: MealRequestStatusBadgeProps) {
  const [statusValue, setStatusValue]
    = useState(StatusValues[props.status]);

  useEffect(() => {
    setStatusValue(StatusValues[props.status]);
  }, [props.status]);

  return (
    <Container>
      <Title>
        Статус заявки:
      </Title>
      <Status $color={statusValue.color}>
        {statusValue.name}
      </Status>
    </Container>
  );
}
