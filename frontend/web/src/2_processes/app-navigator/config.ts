import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../7_shared/config/routes/auth-routes';
import {Role} from '../../7_shared/model/role';

export const ROLE_DEFAULT_ROUTES: {[index: string]: string} = {
  [Role.canteen_staff]: CANTEEN_STAFF_ROUTES.application,
  [Role.teacher]: TEACHER_ROUTES.teacher,
};
