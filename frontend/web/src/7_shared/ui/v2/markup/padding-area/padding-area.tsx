import {PaddingAreaProps} from './props.ts';

export function PaddingArea(props: PaddingAreaProps) {
  return (
    <div style={{
      padding: props.padding
    }}>
      {props.children}
    </div>
  );
}
