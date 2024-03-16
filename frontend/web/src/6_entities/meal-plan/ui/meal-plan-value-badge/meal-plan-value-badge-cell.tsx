import {ValueBadge, ValueBadgeProps} from '../../../../7_shared/ui/v2/value-badge';
import {MealPlanValueBadgeProps} from './props.ts';
import {getStyles} from './get-styles.ts';
import {StyleTypes} from './const.ts';
import {AbstractCell} from '../../../../7_shared/ui/v2/table';
import {Container} from './styles.ts';

export function MealPlanValueBadgeCell({value, type, styles, ...props}: MealPlanValueBadgeProps) {
  return (
    <AbstractCell
      {...props}>
      <Container
        $justifyContent={styles?.justifyContent}
        $padding={styles?.padding}>
        <ValueBadge
          value={value}
          type={type as ValueBadgeProps['type']}
          styles={getStyles(type as StyleTypes)}/>
      </Container>
    </AbstractCell>
  );
}
