import {CheckboxCellProps} from './props.ts';
import {Container} from './styles.ts';
import {AbstractCell} from '../../abstract-cell';
import {Checkbox} from '../../../interactive/check-box';

export function CheckboxCell({children, cellStyles, header, as, key, showContent, styles, ...props}: CheckboxCellProps) {
  return (
    <AbstractCell
      header={header}
      as={as}
      key={key}
      showContent={showContent}
      cellStyles={cellStyles}>
      <Container
        $justifyContent={styles?.justifyContent}>
        <Checkbox
          {...props}/>
        {children}
      </Container>
    </AbstractCell>
  );
}
