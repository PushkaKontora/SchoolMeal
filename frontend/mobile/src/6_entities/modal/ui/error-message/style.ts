import {StyleSheet} from 'react-native';
import {ErrorMessageProps} from "./props";

export const createStyle = (props: ErrorMessageProps) => StyleSheet.create({
    errorMessage: {
        marginTop: 4,
        fontWeight: '400',
        fontSize: 11,
        lineHeight: 13,
        color: props?.displayErrorMessage == true ? '#FFFFFF' : '#EE6725',
    },
});
