import {StyleSheet} from 'react-native';
import {ModalProps} from "../model/props";

export const createStyle = (props: ModalProps) => StyleSheet.create({
    containerContent: {
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        backgroundColor: '#FFFFFF',
        justifyContent: "flex-end",
        marginTop: 'auto',
    },
    container: {
        flex: 1,
    },
    titles: {
        // flexDirection: 'column',
        // gap: 6,
        // alignItems: 'center',
        // marginBottom: 21,
        // marginHorizontal: 'auto',
    },
});
