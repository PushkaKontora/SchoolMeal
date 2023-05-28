import {StyleSheet} from 'react-native';
import {PortionsPartProps} from "./props";

export const createStyle = (props: PortionsPartProps) => StyleSheet.create({
    container: {
        flexDirection: 'row',
        backgroundColor: '#F7F7F7',
        borderRadius: 10,
        gap: 8,
        marginBottom: 4,
        padding: 8,
        alignItems: 'center',
    },
    imageContainer: {
        height: 32,
        width: 32,
        backgroundColor: '#D9D9D9',
        borderRadius: 100,
    },
    image: {
        height: 32,
        width: 32,
    },
    textContainer: {
        flexDirection: 'column',
        gap: 4,
    },
    textPart: {
        fontWeight: '500',
        fontSize: 12,
        lineHeight: 12
    },

    containerModal: {
        backgroundColor: '#FFFFFF',
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        marginTop: 'auto',
    },

});
