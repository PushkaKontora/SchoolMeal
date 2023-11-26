import {PropsWithChildren} from 'react';

export type ModalProps = {
    headerModalTitle: string,
    clickExit: () => void,
} & PropsWithChildren;
