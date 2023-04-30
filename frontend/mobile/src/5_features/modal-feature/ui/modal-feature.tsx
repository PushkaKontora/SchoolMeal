import {ModalProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area';
import {PADDINGS} from '../config/config';
import {ModalHeader} from "../../../6_entities/modal/ui/modal-header/modal-header";
import {ButtonPrimary} from "../../../7_shared/ui/buttons/button-primary";
import {TouchableOpacity, View} from "react-native";
import {MarginArea} from "../../../7_shared/ui/styling/margin-area";

export function ModalFeature(props: ModalProps) {
    const styles = createStyle(props);

    return (
        <View style={styles.container}>
            <PaddingArea
                {...PADDINGS}>
                <ModalHeader
                    headerModalTitle={props.headerModalTitle}
                    clickExit={props.clickExit}/>
                {props.children}
                <TouchableOpacity
                    onPress={props?.functionButton}>
                    <MarginArea marginHorizontal={16}>
                        <ButtonPrimary
                            title={'Сохранить изменения'}
                            onPress={props.functionButton}
                            backgroundColor={'#EC662A'}
                            disabled={props.disabledButton}
                            textColor={'#FFFFFF'}
                            borderRadius={10}/>
                    </MarginArea>
                </TouchableOpacity>
            </PaddingArea>
        </View>
    );
}
