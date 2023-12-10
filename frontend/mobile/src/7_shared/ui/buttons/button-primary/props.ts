import {TextStyle} from 'react-native';

export type ButtonPrimaryProps = {
    title: string,
    onPress?: () => void,
    borderRadius?: number,
    backgroundColor?: string
    textColor?: string,
    disabled?: boolean,
    fontSize?: number,
    fontWeight?: TextStyle['fontWeight'],
    paddingVertical?: number,
    paddingHorizontal?: number,
    flex?: number
};
