import {Route} from 'react-router-dom';
import {CANTEEN_STAFF_ROUTES} from '../../../7_shared/config/routes/auth-routes';
import {PrivateRoute} from '../../../5_features/private-route';
import {MealApplicationPage} from '../../../3_pages/legacy/meal-application-page';
import {Role} from '../../../7_shared/model/role';

export function EmployeeRouter() {
  return (
    <Route
      path={CANTEEN_STAFF_ROUTES.root}>

      <Route
        path={CANTEEN_STAFF_ROUTES.application}
        element={
          <PrivateRoute
            requiredRole={Role.employee}>
            <MealApplicationPage/>
          </PrivateRoute>
        }/>

    </Route>
  );
}
