import {PropsWithChildren} from 'react';

export type ModalProps = {
    headerModalTitle: string,
    functionButton: () => {},
    clickExit: () => {},
    disabledButton: boolean,
    titleButton?: string,
} & PropsWithChildren;
