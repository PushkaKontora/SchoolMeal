import CloseIcon from './assets/close.svg?react';
import GreenTickIcon from './assets/green_tick.svg?react';

import {CloseButtonStyles, ToastStyles, ToastText} from './styles.ts';
import {CloseButtonProps, CustomToastProps} from './props.ts';

export function CloseButton({onClick}: CloseButtonProps) {
  return (
    <CloseButtonStyles onClick={onClick}>
      <CloseIcon/>
    </CloseButtonStyles>
  );
}

export function Toast(props: CustomToastProps) {
  return (
    <ToastStyles>
      <GreenTickIcon
        width={'24px'}
        height={'24px'}/>
      <ToastText>
        {props.message}
      </ToastText>
      <CloseButton
        onClick={() => {
          props.toastProps?.onClose?.(props.toastProps);
          props?.onClose?.();
        }}/>
    </ToastStyles>
  );
}
