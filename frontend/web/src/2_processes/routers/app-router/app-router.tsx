import {Route, Routes} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../7_shared/config/routes/no-auth-routes';
import {LoginPage} from '../../../3_pages/login-page';
import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../../7_shared/config/routes/auth-routes';
import {PrivateRoute} from '../../../5_features/private-route';
import {Role} from '../../../7_shared/model/role';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {TeacherMainPage} from '../../../3_pages/teacher-main-page/ui/teacher-main-page.tsx';

export function AppRouter() {
  return (
    <Routes>
      <Route
        path={NO_AUTH_ROUTES.login}
        element={<LoginPage/>}/>

      <Route
        path={CANTEEN_STAFF_ROUTES.application}
        element={
          <PrivateRoute
            requiredRole={Role.canteen_staff}>
            <MealApplicationPage/>
          </PrivateRoute>
        }/>
      <Route
        path={TEACHER_ROUTES.teacher}
        element={
          <PrivateRoute
            requiredRole={Role.teacher}>
            <TeacherMainPage/>
          </PrivateRoute>
        }/>
    </Routes>
  );
}
