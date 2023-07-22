import {MenuProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: MenuProps) => StyleSheet.create({
    container: {
        backgroundColor: '#FFFFFF',
        borderRadius: 10,
        paddingVertical: 16,
        paddingHorizontal: 16,
        marginTop: 8,
        marginHorizontal: 16,
    },
});
