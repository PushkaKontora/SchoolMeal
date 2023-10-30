import {PropsWithChildren} from 'react';
import {Portions} from '../../../../../../7_shared/model/portions';
import {StyleSheet} from 'react-native';
import NamedStyles = StyleSheet.NamedStyles;

export type PortionsPartProps = {
    imagePath: any,
    portions: Portions
} & PropsWithChildren;

export type InformationModalProps = {
    styles: NamedStyles<any>,
    onExit: () => void
} & PortionsPartProps;
