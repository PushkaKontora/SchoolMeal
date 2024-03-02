import {ButtonContainer, ButtonText} from './styles.ts';
import {LogoutButtonProps} from './props.ts';

export function LogoutButton(props: LogoutButtonProps) {
  return (
    <ButtonContainer
      onClick={props.onClick}>
      {
        props?.icon
      }
      <ButtonText>
        {props.accountName}
      </ButtonText>
    </ButtonContainer>
  );
}
