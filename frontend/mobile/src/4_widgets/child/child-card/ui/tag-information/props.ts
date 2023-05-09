import {PropsWithChildren} from 'react';

export type TagInformationProps = {
    imageTag: any,
    textTag: string,
    borderRadius?: number,
} & PropsWithChildren;
