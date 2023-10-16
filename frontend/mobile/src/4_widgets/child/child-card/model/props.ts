import {PropsWithChildren} from 'react';
import {PropsWithNavigation} from '../../../../7_shared/model/props-with-navigation';
import {Child} from '../../../../6_entities/child/model/child';

export type ChildCardProps = {
    child: Child,
} & PropsWithChildren & PropsWithNavigation;
