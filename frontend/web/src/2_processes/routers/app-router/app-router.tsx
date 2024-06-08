import {Route, Routes} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../3_pages/routing';
import {LoginPage} from '../../../3_pages/login-page';
import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../../3_pages/routing';
import {PrivateRoute, PrivateRouteProps} from '../../../3_pages/routing/private-route';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {MealRequestMonitorPage} from '../../../3_pages/meal-request-monitor-page';
import {Role} from '../../../5_features/auth';
import {AppRouterProps} from './model/props.ts';
import {NutritionClassListPage} from '../../../3_pages/nutrition-class-list-page';
import {IndexRoute} from './index-route.tsx';

const DefaultPrivateRoute = (props: Omit<PrivateRouteProps, 'redirectTo'>) => (
  <PrivateRoute
    {...props}
    redirectTo={NO_AUTH_ROUTES.login}/>
);

export function AppRouter(props: AppRouterProps) {
  return (
    <Routes>
      {/*<Route*/}
      {/*  index*/}
      {/*  path={'/'}*/}
      {/*  element={<IndexRoute/>}*/}
      {/*/>*/}

      <Route
        path={NO_AUTH_ROUTES.login}
        element={<LoginPage {...props.loginPageProps}/>}/>

      <Route
        path={CANTEEN_STAFF_ROUTES.Requests}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.staff}>
            <MealRequestMonitorPage/>
          </DefaultPrivateRoute>
        }/>

      <Route
        path={TEACHER_ROUTES.MyClasses}
        element={
          <DefaultPrivateRoute
            requiredRole={Role.teacher}>
            <NutritionClassListPage/>
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
