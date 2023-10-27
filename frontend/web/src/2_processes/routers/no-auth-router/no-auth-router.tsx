import {Route} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../7_shared/config/routes/no-auth-routes';
import {LoginPage} from '../../../3_pages/login-page';

export function NoAuthRouter() {
  return (
    <Route
      path={NO_AUTH_ROUTES.login}
      element={<LoginPage/>}/>
  );
}
