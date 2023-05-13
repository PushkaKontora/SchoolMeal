import {ChildCardProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: ChildCardProps) => StyleSheet.create({
    container: {
        backgroundColor: '#FFFFFF',
        borderRadius: 10,
        marginTop: 8
    },
    tagContainer: {
        flexDirection: 'column',
        gap: 4,
    },
    titles: {
        flexDirection: 'column',
        gap: 8,
        alignItems: 'center',
        marginBottom: 24
    },
    header: {
        fontWeight: '600',
        fontSize: 28
    },
    subHeader: {
        fontWeight: '400',
        fontSize: 14
    },
    content: {
        flexDirection: 'row',
        gap: 16,

        marginHorizontal: 16,
        marginVertical: 16,
    },
    statusMeal: {
        marginTop: 'auto',
        marginLeft: 'auto',

        fontWeight: '500',
        fontSize: 14,
        lineHeight: 16
    }
});
