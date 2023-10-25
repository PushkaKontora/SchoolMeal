import {PropsWithChildren} from 'react';

export type TextFormProps = {
    functionChangeText: () => void,
} & PropsWithChildren;
