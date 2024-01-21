import {PropsWithChildren} from 'react';

export type ClassItemProps = {
    className: string,
    indexArray: string | number,
} & PropsWithChildren;
