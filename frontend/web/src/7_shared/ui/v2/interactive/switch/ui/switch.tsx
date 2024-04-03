import {SwitchInput, SwitchLabel, SwitchToggle} from './styles.ts';
import {SwitchProps} from '../model/props.ts';

export function Switch(props: SwitchProps) {
  return (
    <SwitchLabel>
      <SwitchInput
        type='checkbox'
        aria-checked={props.toggled}
        disabled={props.disabled}
        onChange={props.onToggle}
      />
      <SwitchToggle
        $toggled={props.toggled}
        $disabled={props.disabled}
      />
    </SwitchLabel>
  );
}
