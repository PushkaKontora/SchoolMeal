import {ModalAddChildProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: ModalAddChildProps) => StyleSheet.create({
    container: {
        flex: 1,
    },
    inputField: {
        backgroundColor: '#FFFFFF',
        borderRadius: 0,
        borderColor: '#E9E9E9',
        borderWidth: 1,
        color: '#212121',
    },
    content: {
        paddingHorizontal: 44,
        paddingVertical: 14,
        width: '100%',
    },
    contentTitle: {
        marginBottom: 8,
        fontWeight: '500',
        fontSize: 14,
        lineHeight: 16,
        color: '#212121'
    },
});
