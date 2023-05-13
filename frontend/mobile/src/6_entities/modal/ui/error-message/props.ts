import {PropsWithChildren} from 'react';

export type ErrorMessageProps = {
    displayErrorMessage: boolean | string,
    textMessage: string
} & PropsWithChildren;
