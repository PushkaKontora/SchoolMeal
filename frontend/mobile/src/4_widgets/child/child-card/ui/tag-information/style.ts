import {StyleSheet} from 'react-native';
import {TagInformationProps} from "./props";

export const createStyle = (props: TagInformationProps) => StyleSheet.create({
    container: {
        flexDirection: 'row',
        gap: 4,

        backgroundColor: '#F0F0F0',
        borderRadius: props.borderRadius || 5,

        paddingVertical: 4,
        paddingHorizontal:  props.paddingHorizontal || 8,
        marginRight: 'auto',
    },
    titles: {
        fontWeight: '400',
        fontSize: 12,
        lineHeight: 14,
        alignItems: "center",
        color: '#212121'
    },
});
