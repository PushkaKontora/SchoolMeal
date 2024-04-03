import {MealPlanStatusBadgeProps} from './props.ts';
import {AbstractCell, ContentContainer} from '../../../../7_shared/ui/v2/table';
import {ValueBadge} from '../../../../7_shared/ui/v2/value-badge';
import {getBadgeType} from './status-utils.ts';

export function MealPlanStatusBadgeCell(props: MealPlanStatusBadgeProps) {
  return (
    <AbstractCell
      {...props.cellProps}>
      <ContentContainer
        $justifyContent={'flex-start'}>
        <ValueBadge
          value={props.status.valueOf()}
          type={getBadgeType(props.status)}
          showDash={true}
        />
      </ContentContainer>
    </AbstractCell>
  );
}
