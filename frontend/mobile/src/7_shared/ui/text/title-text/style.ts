import {StyleSheet} from 'react-native';
import {TitleTextProps} from './props';

export const createStyle = (props: TitleTextProps) => StyleSheet.create({
    default: {
        fontWeight: props.fontWeight || '600',
        fontSize: props.fontSize || 19,
        lineHeight: props.lineHeight || 23,
        color: props.textColor || '#000000',
    },
    container: {
        paddingBottom: props.paddingBottom || 12,
       //width: '100%',
        marginLeft: props.marginLeft || 0,
        alignItems: props.alignItems || 'flex-start',
    }
});
