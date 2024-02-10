import {useEffect, useState} from 'react';

import {CheckboxProps} from '../model/props.ts';
import {CheckboxContainer, CheckboxInput, CheckboxLabel} from '../consts/styles.ts';
import {Tick} from './tick.tsx';

export function Checkbox(props: CheckboxProps) {
  /*
  const [checked, setChecked] = useState(props.checked);
  const [disabled, setDisabled] = useState(props.disabled);

  useEffect(() => {
    setDisabled(props.disabled);
  }, [props.disabled]);

  useEffect(() => {
    setChecked(props.checked);
  }, [props.checked]);
  */

  return (
    <CheckboxLabel>
      <CheckboxInput
        type='checkbox'
        aria-checked={props.checked}
        onChange={props.onChange}
        disabled={props.disabled}/>
      <CheckboxContainer
        $disabled={props.disabled}
        $checked={props.checked}>
        {props.checked && <Tick/>}
      </CheckboxContainer>
    </CheckboxLabel>
  );
}
