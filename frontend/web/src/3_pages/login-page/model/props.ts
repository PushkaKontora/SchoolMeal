import {
  AccessTokenOut
} from '../../../7_shared/api/implementations/v3/backend-types/user-management/access-token-out.ts';
import {Role} from '../../../7_shared/lib/auth';

export type LoginPageProps = {
  onSuccess: (response: AccessTokenOut) => void | Promise<void>,
  onError?: () => void,
  onAuthorized?: (role?: Role) => void
};
