import {MealUnitProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: MealUnitProps) => StyleSheet.create({
    container: {
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5E5',
        paddingBottom: 8,
        marginBottom: 16,
        marginTop: 14,
    },
    title: {
        flexDirection: 'row',
    }
});
