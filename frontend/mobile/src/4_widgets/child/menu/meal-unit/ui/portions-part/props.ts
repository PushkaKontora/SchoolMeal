import {PropsWithChildren} from 'react';
import {ImageSourcePropType, StyleSheet} from 'react-native';
import NamedStyles = StyleSheet.NamedStyles;
import {Food} from '../../../../../../7_shared/model/food';

export type PortionsPartProps = {
    imagePath: ImageSourcePropType,
    food: Food
} & PropsWithChildren;

export type InformationModalProps = {
    styles: NamedStyles<any>,
    onExit: () => void
} & PortionsPartProps;
