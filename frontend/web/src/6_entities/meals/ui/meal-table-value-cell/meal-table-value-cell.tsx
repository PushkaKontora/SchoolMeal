import {Row} from './styles';
import {ValueBadge} from '../../../../7_shared/ui/special/value-badge';
import {MealTableValueCellProps} from './props';
import {TOTAL_STYLES} from './config';

export function MealTableValueCell(props: MealTableValueCellProps) {
  return (
    <Row
      backgroundColor={props.backgroundColor}
      borderRadius={props.borderRadius}>
      <td>
        <ValueBadge
          value={props.paid}/>
      </td>
      <td>
        <ValueBadge
          value={props.preferential}/>
      </td>
      <td>
        <ValueBadge
          backgroundColor={TOTAL_STYLES.backgroundColor}
          textColor={TOTAL_STYLES.color}
          value={props.total}/>
      </td>
    </Row>
  );
}
