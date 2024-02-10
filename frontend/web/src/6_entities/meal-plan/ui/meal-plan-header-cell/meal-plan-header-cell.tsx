import {AbstractCell} from '../../../../7_shared/ui/v2/table';
import {MealPlanHeaderCellProps} from './props.ts';
import {Container, Price, Title} from './styles.ts';

export function MealPlanHeaderCell({title, price, ...props}: MealPlanHeaderCellProps) {
  return (
    <AbstractCell
      {...props}
      header>
      <Container>
        <Title>
          {title}
        </Title>
        <Price>
          {price}
        </Price>
      </Container>
    </AbstractCell>
  );
}
