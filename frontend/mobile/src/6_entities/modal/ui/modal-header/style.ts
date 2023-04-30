import {StyleSheet} from 'react-native';
import {ModalHeaderProps} from "./props";

export const createStyle = (props: ModalHeaderProps) => StyleSheet.create({
    headerContent:{
        flexDirection: 'row',
        gap: 69,
        marginBottom: 16,

        borderBottomColor: '#F3F3F3',
        borderBottomWidth: 0.7,
    },
    headerTitle: {
        fontWeight: '700',
        fontSize: 16,
        lineHeight: 18,

        color: '#212121',
    },
});
