import {LoginFormData} from '../../5_features/auth-forms/ui/login-form/types.ts';

export type LoginWidgetProps = {
  onSubmit: (formData: LoginFormData) => void,
  disabled: boolean
}
