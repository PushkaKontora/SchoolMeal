import {ButtonPrimaryProps} from './props.ts';
import {useEffect, useState} from 'react';
import {ButtonContainer} from './styles.ts';

export function ButtonPrimary(props: ButtonPrimaryProps) {
  const [disabled, setDisabled] = useState(Boolean(props.disabled));

  useEffect(() => {
    setDisabled(Boolean(props.disabled));
  }, [props.disabled]);

  return (
    <ButtonContainer
      $borderRadius={props.borderRadius}
      $backgroundColor={props.backgroundColor}
      $textColor={props.textColor}
      $fontSize={props.fontSize}
      $fontFamily={props.fontFamily}
      $paddingVertical={props.paddingVertical}
      $paddingHorizontal={props.paddingHorizontal}
      onClick={props.onPress}
      disabled={disabled}>
      {props.title}
    </ButtonContainer>
  );
}
