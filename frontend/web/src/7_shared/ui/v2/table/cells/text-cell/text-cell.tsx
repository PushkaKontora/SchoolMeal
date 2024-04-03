import {TextCellProps} from './props.ts';
import {Container} from './styles.ts';
import {AbstractCell} from '../../abstract-cell';

export function TextCell({cellProps, styles, text}: TextCellProps) {
  return (
    <AbstractCell
      {...cellProps}>
      <Container
        $justifyContent={styles?.justifyContent}
        $padding={styles?.padding}
        $header={cellProps.header}>
        {text}
      </Container>
    </AbstractCell>
  );
}