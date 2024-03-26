import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../index.ts';
import {Role} from '../../../5_features/auth';

export const ROLE_DEFAULT_ROUTES: {[index: string]: string} = {
  [Role.staff]: CANTEEN_STAFF_ROUTES.Requests,
  [Role.teacher]: TEACHER_ROUTES.MyClasses,
};
