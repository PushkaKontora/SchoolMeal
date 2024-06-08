import {ButtonPrimaryProps} from './props';
import {useEffect, useState} from 'react';
import {ButtonContainer} from './styles';

export function ButtonPrimary(props: ButtonPrimaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  useEffect(() => {
    setDisabled(Boolean(props.disabled));
  }, [props.disabled]);

  return (
    <ButtonContainer
      onClick={props.onPress}
      fontSize={props.fontSize}
      disabled={disabled}>
      {props.title}
    </ButtonContainer>
  );
}
