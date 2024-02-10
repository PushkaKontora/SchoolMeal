import {TextCellProps} from './props.ts';
import {Container} from './styles.ts';
import {AbstractCell} from '../../abstract-cell';

export function TextCell({cellStyles, styles, header, as, key, text}: TextCellProps) {
  return (
    <AbstractCell
      header={header}
      as={as}
      key={key}
      cellStyles={cellStyles}>
      <Container
        $justifyContent={styles?.justifyContent}
        $padding={styles?.padding}
        $header={header}>
        {text}
      </Container>
    </AbstractCell>
  );
}