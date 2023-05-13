import {PropsWithChildren} from "react";

export type ModalHeaderProps = {
    headerModalTitle: string,
    clickExit: () => {},
} & PropsWithChildren;
