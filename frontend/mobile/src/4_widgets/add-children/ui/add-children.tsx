import {SUB_EMOJI_TITLE} from '../consts/consts';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary/button-primary';
import {EmojiTextFeature} from '../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import {magicModal, MagicModalPortal} from "react-native-magic-modal";
import {ModalAddChildProps} from "../model/props";
import {createStyle} from "../consts/styleModal";
import {ModalFeature} from "../../../5_features/modal-feature/ui/modal-feature";
import {useState} from "react";
import {Text, View} from "react-native";
import {InputField} from "../../../7_shared/ui/fields/input-field";
import {INPUT_DATA} from "../inputData";
import {Controller, useForm} from "react-hook-form";
import {idChildData} from "../types";
import {ErrorMessage} from "../../../6_entities/modal/ui/error-message/error-message";
import {ControlledInputField} from "../../../6_entities/controlled/controlled-input-field";
import {SignUpFormData} from "../../../6_entities/user/ui/sign-up-form/types";


export function AddChildrenWidget(props: ModalAddChildProps) {
    const [idChild, setIdChild] = useState('');
    const [disabled, setDisabled] = useState(true);
    const [invisibleErrorMessage, setInvisibleErrorMessage] = useState(true);
    const {
        handleSubmit,
        control,
        formState: {errors}
    } = useForm<SignUpFormData>({
        mode: 'onChange'
    });
    const item = {
        name: 'name',
        label: 'id',
        type: '',
        options: {
            required: 'Вы не заполнили это поле'
        },
        placeholder: ''
    };

    const styles = createStyle(props);
    const ConfirmationModal = () => (
        <ModalFeature
            headerModalTitle={'Добавить ребёнка'}
            functionButton={() => magicModal.hide()}
            disabledButton={disabled}
            clickExit={() => magicModal.hide()}>
            <View style={styles.content}>
                <Text style={styles.contentTitle}>
                    Идентификатор, выданный в школе
                </Text>
                <ControlledInputField
                    key={item.name}
                    control={control}
                    errors={errors}
                    data={item}/>
                <ErrorMessage
                    displayErrorMessage={invisibleErrorMessage}
                    textMessage={'Индентификатора не существует'}/>
            </View>
        </ModalFeature>
    );

    const handleAddChild = () => {
        return magicModal.show(ConfirmationModal);
    };

    return (
        <EmojiTextFeature
            imageEmoji={require('../../../5_features/emoji-text-feature/images/angelAmoji.png')}
            subEmojiTitle={SUB_EMOJI_TITLE}>
            <ButtonPrimary
                title={'Добавить ребёнка'}
                onPress={handleAddChild}
                backgroundColor={'#EC662A'}
                textColor={'#FFFFFF'}
                borderRadius={10}/>
            <MagicModalPortal/>
        </EmojiTextFeature>
    );
}
