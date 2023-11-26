import {SymbolCounterProps} from '../model/props';

export function createString(props: SymbolCounterProps) {
  return `${props.currentSymbols}/${props.limit}`;
}
