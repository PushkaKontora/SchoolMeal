import {AbstractCell} from '../../../../7_shared/ui/v2/table';
import {MealPlanHeaderCellProps} from './props.ts';
import {Container, Title} from './styles.ts';

export function MealPlanHeaderCell({title, ...props}: MealPlanHeaderCellProps) {
  return (
    <AbstractCell
      {...props}
      header>
      <Container>
        <Title>
          {title}
        </Title>
      </Container>
    </AbstractCell>
  );
}
