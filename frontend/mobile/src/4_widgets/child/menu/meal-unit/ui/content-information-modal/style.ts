import {StyleSheet} from 'react-native';
import {ContentInformationModalProps} from "./props";

export const createStyle = (props: ContentInformationModalProps) => StyleSheet.create({
    container: {
        flexDirection: 'column',
        gap: 14,
        marginBottom: 25,
        marginHorizontal: 30,
        marginTop: 4,
    },
    containerMainInfo: {
        flexDirection: 'column',
        gap: 4,
    },
    containerImage: {
        width: 80,
        height: 80,
        borderRadius: 10,
    },
    image: {
        width: 80,
        height: 80,
        borderRadius: 100,
    },
    containerMainText: {
        flexDirection: 'row',
        gap: 2,
        alignItems: "flex-end",
    },
    priceText: {
        fontWeight: '700',
        fontSize: 16,
        lineHeight: 24,
        color: '#FF692C',
    },
    weightText: {
        fontWeight: '500',
        fontSize: 11,
        lineHeight: 21,
        color: '#9A9A9A',
    },
    containerDetailComposition: {
        flexDirection: 'row',
        gap: 26,
    },
    item: {
        fontWeight: '500',
        fontSize: 14,
        lineHeight: 16,
        color: '#212121',
    },
    nameItem: {
        fontWeight: '400',
        fontSize: 12,
        lineHeight: 14,
        color: '#212121',
    },
    nameCompound: {
        fontWeight: '500',
        fontSize: 16,
        lineHeight: 18,
        color: '#212121',
        marginBottom: 4,
    },
    compound: {
        fontWeight: '400',
        fontSize: 12,
        lineHeight: 14,
        color: '#212121',
    },
});
