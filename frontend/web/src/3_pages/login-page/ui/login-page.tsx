import {LoginWidget} from '../../../4_widgets/login-widget';
import {LoginPageProps} from '../model/props.ts';
import {LoginFormData} from '../../../5_features/auth-forms/ui/login-form/types.ts';
import {Api} from '../../../7_shared/api';
import {useState} from 'react';

export function LoginPage(props: LoginPageProps) {
  const [login] = Api.useLoginMutation();

  const [disabled, setDisabled] = useState(false);

  const onSubmit = (formData: LoginFormData) => {
    setDisabled(true);
    login({
      ...formData,
      fingerprint: 'aaaaa'
    })
      .unwrap()
      .then(response => {
        props.onSuccess(response);
      })
      .catch(() => {
        props.onError?.();
        setDisabled(false);
      });
  };

  return (
    <LoginWidget
      onSubmit={onSubmit}
      disabled={disabled}
    />
  );
}
