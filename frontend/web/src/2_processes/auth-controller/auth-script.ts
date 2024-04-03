import {useAppDispatch} from '../../../store/hooks.ts';
import {AuthTokenProcessor} from '../../5_features/auth';
import {setAuthorized} from '../../5_features/auth/model/auth-slice/auth-slice.ts';

export async function checkToken(dispatch: ReturnType<typeof useAppDispatch>) {
  await AuthTokenProcessor.getAuthToken()
    .then(async (value) => {
      const result = value !== null;

      dispatch(setAuthorized(result));
    })
    .catch(() => dispatch(setAuthorized(false)));
}
