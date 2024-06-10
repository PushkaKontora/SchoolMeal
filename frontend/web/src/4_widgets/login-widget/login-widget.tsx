import { Content } from '../../7_shared/ui/markup/content';
import { LoginForm } from '../../5_features/auth-forms/ui/login-form';
import { LoginFormData } from '../../5_features/auth-forms/ui/login-form/types';
import {LoginWidgetProps} from './props.ts';
import LogoSvg from './assets/logo.svg?react';
import {PaddingArea} from '../../7_shared/ui/v2/markup/padding-area';
import {LoginFormTitle} from './styles.ts';

export function LoginWidget(props: LoginWidgetProps) {
  const onSubmit = async (formData: LoginFormData) => {
    props.onSubmit(formData);
  };

  return (
    <Content width={'100%'}>
      <PaddingArea
        padding={'32px 0 0 16px'}>
        <LogoSvg
          width={'246px'}
          height={'33px'}/>
        <LoginFormTitle>
          Войдите в свой профиль
        </LoginFormTitle>
        <LoginForm onSubmit={onSubmit} />
      </PaddingArea>
    </Content>
  );
}
