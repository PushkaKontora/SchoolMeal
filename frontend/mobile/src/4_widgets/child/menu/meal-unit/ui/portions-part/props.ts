import {PropsWithChildren} from 'react';
import {Portions} from '../../../../../../7_shared/model/portions';

export type PortionsPartProps = {
    imagePath: any,
    portions: Portions
} & PropsWithChildren;
