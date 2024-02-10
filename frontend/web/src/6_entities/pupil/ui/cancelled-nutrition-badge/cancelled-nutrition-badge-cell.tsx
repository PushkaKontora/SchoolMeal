import {BadgeCellProps} from './props.ts';
import {AbstractCell} from '../../../../7_shared/ui/v2/table';
import {CancelledNutritionBadge} from './cancelled-nutrition-badge.tsx';

export function CancelledNutritionBadgeCell({text, cancelled, ...props}: BadgeCellProps) {
  return (
    <AbstractCell
      {...props}>
      {
        cancelled ? (
          <CancelledNutritionBadge text={text}/>
        ) : null
      }
    </AbstractCell>
  );
}
