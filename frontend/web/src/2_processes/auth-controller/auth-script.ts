import {useAppDispatch} from '../../../store/hooks.ts';
import {setAuthorized} from '../../7_shared/lib/auth/model/auth-slice/auth-slice.ts';
import {AuthTokenProcessor} from '../../7_shared/lib/auth';

export async function checkToken(dispatch: ReturnType<typeof useAppDispatch>) {
  await AuthTokenProcessor.getAuthToken()
    .then(async (value) => {
      const result = value !== null;

      dispatch(setAuthorized(result));
    })
    .catch(() => dispatch(setAuthorized(false)));
}
