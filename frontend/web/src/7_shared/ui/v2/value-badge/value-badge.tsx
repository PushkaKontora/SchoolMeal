import {BadgeContainer} from './styles';
import {ValueBadgeProps} from './props';
import {applyShowDashProp, getStylesFromType} from './lib.ts';

export function ValueBadge({value, type, ...props}: ValueBadgeProps) {
  const styles = {
    ...getStylesFromType(type),
    ...props.styles
  };

  return (
    <BadgeContainer
      $backgroundColor={styles?.backgroundColor}
      $textColor={styles?.textColor}
      $margin={styles?.margin}
      $fontFamily={styles?.fontFamily}
      $width={styles?.width}>
      {applyShowDashProp(props.showDash)(value) ? value : '\u00A0\u0336\u00A0'}
    </BadgeContainer>
  );
}
