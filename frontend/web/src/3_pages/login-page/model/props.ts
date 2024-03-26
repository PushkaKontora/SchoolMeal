import {
  AccessTokenOut
} from '../../../7_shared/api/implementations/v3/backend-types/user-management/access-token-out.ts';

export type LoginPageProps = {
  onSuccess: (response: AccessTokenOut) => void | Promise<void>,
  onError?: () => void
};
