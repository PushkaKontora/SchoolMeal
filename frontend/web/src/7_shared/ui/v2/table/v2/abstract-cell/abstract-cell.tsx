import {AbstractCellProps} from './props.ts';
import {Cell} from './styles.ts';

export function AbstractCell({children, cellStyles, header, as, key, showContent}: AbstractCellProps) {
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
      scope={'col'}>
      <div style={{
        visibility: (showContent ?? true) ? 'visible' : 'hidden'
      }}>
        {children}
      </div>
    </Cell>
  );
}
