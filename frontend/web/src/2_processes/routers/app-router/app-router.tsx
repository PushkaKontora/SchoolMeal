import {Route, Routes} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../7_shared/config/routes/no-auth-routes';
import {LoginPage} from '../../../3_pages/login-page';
import {EMPLOYEE_ROUTES} from '../../../7_shared/config/routes/auth-routes';
import {PrivateRoute} from '../../../5_features/private-route';
import {Role} from '../../../7_shared/model/role';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {LoadingPage} from '../../../3_pages/loading-page';

export function AppRouter() {
  return (
    <Routes>
      <Route
        path={NO_AUTH_ROUTES.login}
        element={<LoginPage/>}/>

      <Route
        path={EMPLOYEE_ROUTES.application}
        element={
          <PrivateRoute
            requiredRole={Role.employee}>
            <MealApplicationPage/>
          </PrivateRoute>
        }/>
    </Routes>
  );
}
