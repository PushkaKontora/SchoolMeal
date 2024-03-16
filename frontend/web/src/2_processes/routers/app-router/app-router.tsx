import {Route, Routes} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../3_pages/routing';
import {LoginPage} from '../../../3_pages/login-page';
import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../../3_pages/routing';
import {PrivateRoute, PrivateRouteProps} from '../../../5_features/private-route';
import {Role} from '../../../7_shared/model/role';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {MealRequestMonitorPage} from '../../../3_pages/meal-request-monitor-page/ui/meal-request-monitor-page.tsx';

const DefaultPrivateRoute = (props: Omit<PrivateRouteProps, 'redirectTo'>) => (
  <PrivateRoute
    {...props}
    redirectTo={NO_AUTH_ROUTES.login}/>
);

export function AppRouter() {
  return (
    <Routes>
      <Route
        path={NO_AUTH_ROUTES.login}
        element={<LoginPage/>}/>

      <Route
        path={CANTEEN_STAFF_ROUTES.Requests}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.canteen_staff}>
            <MealRequestMonitorPage/>
          </DefaultPrivateRoute>
        }/>

      <Route
        path={TEACHER_ROUTES.MyClasses}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.teacher}>
            {'Мои классы'}
          </DefaultPrivateRoute>
        }/>
      <Route
        path={TEACHER_ROUTES.ApplyRequest}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.teacher}>
            <MealApplicationPage/>
          </DefaultPrivateRoute>
        }/>
      <Route
        path={TEACHER_ROUTES.History}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.teacher}>
            {'История заявок'}
          </DefaultPrivateRoute>
        }/>
    </Routes>
  );
}
