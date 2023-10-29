import {PropsWithChildren} from 'react';
import {PropsWithNavigation} from '../../../7_shared/model/props-with-navigation';
import {FormControl, FormErrors} from '../../../7_shared/model/forms/form-types';

export type ModalAddChildProps = PropsWithChildren & PropsWithNavigation;

export type ConfirmationModalStyles = {
    content: object,
    contentTitle: object,
    inputField: object
};

export type ConfirmationModalProps = {
    onConfirm: () => void,
    onClose: () => void,
    confirmDisabled: boolean,
    styles: ConfirmationModalStyles,
    control: FormControl,
    errors: FormErrors,
    displayError: boolean
};
