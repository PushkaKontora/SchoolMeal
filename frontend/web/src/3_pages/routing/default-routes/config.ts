import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../index.ts';
import {Role} from '../../../7_shared/model/role.ts';

export const ROLE_DEFAULT_ROUTES: {[index: string]: string} = {
  [Role.canteen_staff]: CANTEEN_STAFF_ROUTES.Requests,
  [Role.teacher]: TEACHER_ROUTES.MyClasses,
};
