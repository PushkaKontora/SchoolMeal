import {PropsWithChildren} from 'react';

export type ModalProps = {
    headerModalTitle: string,
    functionButton: () => {},
    clickExit: () => {},
    disabledButton: boolean,
    buttonTitle: string
} & PropsWithChildren;
