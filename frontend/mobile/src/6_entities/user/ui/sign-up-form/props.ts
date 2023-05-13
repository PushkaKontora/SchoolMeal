import {SignUpFormData} from './types';

export type SignUpFormProps = {
  onSubmit: (data: SignUpFormData) => void,
  onError: (msg: any) => void
};