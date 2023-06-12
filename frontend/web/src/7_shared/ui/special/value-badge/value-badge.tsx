import {BadgeContainer} from './styles';
import {ValueBadgeProps} from './props';

export function ValueBadge(props: ValueBadgeProps) {
  const {value, ...styles} = props;

  return (
    <BadgeContainer
      {...styles}>
      {value}
    </BadgeContainer>
  );
}
