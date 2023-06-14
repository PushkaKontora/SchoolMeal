import {Image, ImageBackground, Text, TouchableOpacity, View} from 'react-native';
import {PortionsPartProps} from './props';
import {createStyle} from './style';
import {magicModal} from "react-native-magic-modal";
import {ModalHeader} from "../../../../../../6_entities/modal/ui/modal-header/modal-header";
import {ContentInformationModal} from "../content-information-modal/content-information-modal";

export function PortionsPart(props: PortionsPartProps) {
    const styles = createStyle(props);

    const openInformationPortions = () => {
        return magicModal.show(InformationModal);
    };

    const clickExit = (): any => {
        magicModal.hide();
    };

    const InformationModal = () => (
        <View style={styles.containerModal}>
            <ModalHeader
                headerModalTitle={props.portions.food.name}
                clickExit={clickExit}/>
            <ContentInformationModal imagePath={props.imagePath} portions={props.portions}/>
        </View>
    );

    return (
        <TouchableOpacity onPress={openInformationPortions}
                          style={styles.container}>
            <View style={styles.container}>
                <View style={styles.imageContainer}>
                    <ImageBackground source={require('../../../../../../7_shared/assets/images/Rectangle.png')}
                                     style={{width: '100%', height: '100%'}}>
                        <Image source={{uri: props.imagePath}} style={styles.image}/>
                    </ImageBackground>
                </View>
                <View style={styles.textContainer}>
                    <Text style={styles.textPart}>{props.portions.food.name}</Text>
                    <Text style={styles.textPart}>{props.portions.weight} г</Text>
                </View>
            </View>
        </TouchableOpacity>
    );
}
