import {StyleSheet} from 'react-native';
import {ModalProps} from "../model/props";

export const createStyle = (props: ModalProps) => StyleSheet.create({
    container: {
        backgroundColor: '#FFFFFF',
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        marginTop: 'auto',
    },
    titles: {
        // flexDirection: 'column',
        // gap: 6,
        // alignItems: 'center',
        // marginBottom: 21,
        // marginHorizontal: 'auto',
    },
});
