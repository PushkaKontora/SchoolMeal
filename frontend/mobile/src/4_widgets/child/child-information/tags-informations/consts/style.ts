import {TagsInformationProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: TagsInformationProps) => StyleSheet.create({
    container: {
        flexDirection: 'column',
        gap: 4,
        alignItems: 'flex-start',
        justifyContent: 'flex-start',
        paddingTop: 8,
        paddingBottom: 16,
    },
    first: {
        flexDirection: 'row',
        gap: 4,
    },
    second: {
        marginBottom: 'auto'
    }
});
