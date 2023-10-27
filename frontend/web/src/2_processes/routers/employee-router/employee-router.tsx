import {Route} from 'react-router-dom';
import {EMPLOYEE_ROUTES} from '../../../7_shared/config/routes/auth-routes';
import {PrivateRoute} from '../../../5_features/private-route';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {Role} from '../../../7_shared/model/role';

export function EmployeeRouter() {
  return (
    <Route
      path={EMPLOYEE_ROUTES.root}>

      <Route
        path={EMPLOYEE_ROUTES.application}
        element={
          <PrivateRoute
            requiredRole={Role.employee}>
            <MealApplicationPage/>
          </PrivateRoute>
        }/>

    </Route>
  );
}
