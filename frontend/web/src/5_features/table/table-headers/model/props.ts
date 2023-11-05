import {PropsWithChildren} from 'react';

export type TableHeadersProps = {
    price: string[] | number[]
} & PropsWithChildren;
