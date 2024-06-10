import {LoginWidget} from '../../../4_widgets/login-widget';
import {LoginPageProps} from '../model/props.ts';
import {LoginFormData} from '../../../5_features/auth-forms/ui/login-form/types.ts';
import {Api} from '../../../7_shared/api';

export function LoginPage(props: LoginPageProps) {
  const [login] = Api.useLoginMutation();

  const onSubmit = (formData: LoginFormData) => {
    login({
      ...formData,
      fingerprint: 'aaaaa'
    })
      .unwrap()
      .then(response => {
        props.onSuccess(response);
      })
      .catch(() => props.onError?.());
  };

  return (
    <LoginWidget
      onSubmit={onSubmit}/>
  );
}
