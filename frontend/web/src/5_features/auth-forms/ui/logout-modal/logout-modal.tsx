import {LogoutModalProps} from './props.ts';
import {LogoutButtons, LogoutContainer, LogoutWindow, LogoutWindowContent, LogoutWindowMessage} from './styles.ts';
import {ButtonSecondary} from '../../../../7_shared/ui/v2/interactive/buttons/button-secondary';
import {ButtonPrimary} from '../../../../7_shared/ui/v2/interactive/buttons/button-primary';
import CloseSvg from './assets/close.svg?react';

export function LogoutModal(props: LogoutModalProps) {
  return (
    <LogoutContainer
      $hidden={props.hidden}>
      <LogoutWindow>
        <CloseSvg
          width={'28px'}
          height={'28px'}
          onClick={props.onCancel}
        />

        <LogoutWindowContent>
          <LogoutWindowMessage>
            Вы действительно хотите выйти из аккаунта?
          </LogoutWindowMessage>
          <LogoutButtons>
            <ButtonSecondary
              title={'Остаться'}
              backgroundColor={'#F5F5F5'}
              borderColor={'#00000000'}
              borderRadius={'12px'}
              flex={1}
              onPress={props.onCancel}/>
            <ButtonPrimary
              title={'Выйти'}
              borderRadius={'12px'}
              flex={1}
              onPress={props.onSubmit}/>
          </LogoutButtons>
        </LogoutWindowContent>
      </LogoutWindow>
    </LogoutContainer>
  );
}
