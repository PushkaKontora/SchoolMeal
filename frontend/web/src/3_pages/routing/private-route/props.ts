import {PropsWithChildren} from 'react';
import {RoleOrAny} from './types.ts';

export type PrivateRouteProps = {
  requiredRole: RoleOrAny,
  redirectTo: string
} & PropsWithChildren;
