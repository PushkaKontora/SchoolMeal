import {PropsWithChildren} from 'react';

export type TagsInformationProps = {
    school: string,
    class: string,
    status: string,
} & PropsWithChildren;
