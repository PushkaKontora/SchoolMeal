import {AbstractCellProps} from './props.ts';
import {Cell} from './styles.ts';

export function AbstractCell({children, cellStyles, header, as, key, showContent, ...props}: AbstractCellProps) {
  return (
    <Cell
      key={key}
      as={as ? as : (header ? 'th' : 'td')}
      $header={header}
      $height={cellStyles?.height}
      $backgroundColor={cellStyles?.backgroundColor}
      $fontFamily={cellStyles?.fontFamily}
      $width={cellStyles?.width}
      $minWidth={cellStyles?.minWidth}
      $maxWidth={cellStyles?.maxWidth}
      $whiteSpace={cellStyles?.whiteSpace}
      scope={'col'}
      colSpan={props.columnSpan}
      rowSpan={props.rowSpan}>
      <div style={{
        visibility: (showContent ?? true) ? 'visible' : 'hidden'
      }}>
        {children}
      </div>
    </Cell>
  );
}
