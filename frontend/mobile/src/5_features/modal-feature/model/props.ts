import {PropsWithChildren} from 'react';

export type ModalProps = {
    headerModalTitle: string,
    functionButton: () => void,
    clickExit: () => void,
    disabledButton: boolean,
    buttonTitle?: string
} & PropsWithChildren;
