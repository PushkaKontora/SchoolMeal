import {BadgeProps} from './props.ts';
import {BadgeContainer} from './styles.ts';

export function CancelledNutritionBadge(props: BadgeProps) {
  return (
    <BadgeContainer>
      {props.text}
    </BadgeContainer>
  );
}
