import {ButtonSecondaryProps} from './props.ts';
import {useEffect, useState} from 'react';
import {ButtonContainer} from './styles.ts';

export function ButtonSecondary(props: ButtonSecondaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  useEffect(() => {
    setDisabled(Boolean(props.disabled));
  }, [props.disabled]);

  return (
    <ButtonContainer
      onClick={props.onPress}
      {...props}
      disabled={disabled}>
      {props.title}
    </ButtonContainer>
  );
}
