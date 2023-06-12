import {ButtonSecondaryProps} from './props';
import {useEffect, useState} from 'react';
import {ButtonContainer} from './styles';

export function ButtonSecondary(props: ButtonSecondaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  useEffect(() => {
    setDisabled(Boolean(props.disabled));
  }, [props.disabled]);

  return (
    <ButtonContainer
      onClick={props.onPress}
      disabled={disabled}>
      {props.title}
    </ButtonContainer>
  );
}
