import {ModalAddChildProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: ModalAddChildProps) => StyleSheet.create({
    container: {},
    inputField: {
        backgroundColor: '#FFFFFF',
        borderRadius: 0,
        width: '10',
        borderColor: '#E9E9E9',
        borderWidth: 1,

        color: '#B1B1B1',
    },
    content: {
        marginHorizontal: 44,
        paddingVertical: 14,
    },
    contentTitle: {
        marginBottom: 8,
        fontWeight: '500',
        fontSize: 14,
        lineHeight: 16,
        color: '#212121'
    },
});
