import {LogoutModalProps} from './props.ts';
import {LogoutButtons, LogoutContainer, LogoutWindow, LogoutWindowContent, LogoutWindowMessage} from './styles.ts';
import {ButtonSecondary} from '../../../../7_shared/ui/v2/interactive/buttons/button-secondary';
import {ButtonPrimary} from '../../../../7_shared/ui/v2/interactive/buttons/button-primary';
import CloseSvg from './assets/close.svg?react';

export function LogoutModal(props: LogoutModalProps) {
  return (
    <LogoutContainer>
      <LogoutWindow>
        <CloseSvg
          width={'28px'}
          height={'28px'}
        />

        <LogoutWindowContent>
          <LogoutWindowMessage>
            Вы действительно хотите выйти из аккаунта?
          </LogoutWindowMessage>
          <LogoutButtons>
            <ButtonSecondary
              title={'Остаться'}
              onPress={props.onCancel}/>
            <ButtonPrimary
              title={'Выйти'}
              onPress={props.onSubmit}/>
          </LogoutButtons>
        </LogoutWindowContent>
      </LogoutWindow>
    </LogoutContainer>
  );
}
