import {LoginFormData} from './types';

export type LoginFormProps = {
  onSubmit: (data: LoginFormData) => void,
  onError?: (msg: any) => void,
  disabled: boolean
};
