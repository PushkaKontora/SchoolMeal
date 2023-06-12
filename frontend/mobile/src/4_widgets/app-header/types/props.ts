import {PropsWithChildren} from 'react';
import {PropsWithNavigation} from '../../../7_shared/model/props-with-navigation';
import {StackHeaderProps} from '@react-navigation/stack';

export type AppHeaderProps = {
    title: string,
    showBackButton: boolean
  } &
  StackHeaderProps &
  PropsWithChildren &
  PropsWithNavigation;
