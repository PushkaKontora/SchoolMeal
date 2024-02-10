import {AbstractCell} from '../../abstract-cell';
import {ValueBadgeCellProps} from './props.ts';
import {Container} from './styles.ts';
import {ValueBadge} from '../../../../value-badge';

export function ValueBadgeCell({cellStyles, styles, header, as, key, badgeProps}: ValueBadgeCellProps) {
  return (
    <AbstractCell
      header={header}
      as={as}
      key={key}
      cellStyles={cellStyles}>
      <Container
        $justifyContent={styles?.justifyContent}
        $padding={styles?.padding}>
        <ValueBadge
          value={badgeProps?.value}
          type={badgeProps?.type}/>
      </Container>
    </AbstractCell>
  );
}
