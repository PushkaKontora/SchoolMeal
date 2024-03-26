import { Content } from '../../7_shared/ui/markup/content';
import { LoginForm } from '../../5_features/auth/ui/login-form';
import { LoginFormData } from '../../5_features/auth/ui/login-form/types';
import {LoginWidgetProps} from './props.ts';


export function LoginWidget(props: LoginWidgetProps) {
  const onSubmit = async (formData: LoginFormData) => {
    props.onSubmit(formData);
  };

  return (
    <Content>
      <LoginForm onSubmit={onSubmit} />
    </Content>
  );
}
