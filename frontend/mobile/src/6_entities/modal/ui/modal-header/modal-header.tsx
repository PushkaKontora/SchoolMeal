import {Button, Image, Text, TouchableOpacity} from 'react-native';
import {ModalHeaderProps} from './props';
import {createStyle} from './style';
import {PaddingArea} from "../../../../7_shared/ui/styling/padding-area";
import {PADDINGS_HEADER} from "./config";

export function ModalHeader(props: ModalHeaderProps) {
    const styles = createStyle(props);

    return (
        <PaddingArea
            style={styles.headerContent}
            {...PADDINGS_HEADER}>
            <TouchableOpacity
                style={styles.image}
                onPress={props?.clickExit}>
                <Image onAccessibilityTap={props?.clickExit}
                       source={require('../../../../7_shared/assets/images/exit.png')}/>
            </TouchableOpacity>
            <Text style={styles.headerTitle}>{props.headerModalTitle}</Text>
        </PaddingArea>
    );
}
