import {SUB_EMOJI_TITLE} from '../consts/consts';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary/button-primary';
import {EmojiTextFeature} from '../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import {magicModal, MagicModalPortal} from "react-native-magic-modal";
import {ModalAddChildProps} from "../model/props";
import {createStyle} from "../consts/styleModal";
import {ModalFeature} from "../../../5_features/modal-feature/ui/modal-feature";
import {useState} from "react";
import {Text, View} from "react-native";
import {useForm} from "react-hook-form";
import {ErrorMessage} from "../../../6_entities/modal/ui/error-message/error-message";
import {ControlledInputField} from "../../../6_entities/controlled/controlled-input-field";
import {useGetUserChildQuery, useFindChildOnIDMutation} from "../../../6_entities/child/api/config";
import {idChildData} from "../types";
import {INPUT_DATA} from "../inputData";


export function AddChildrenWidget(props: ModalAddChildProps) {
    const {data: userChild} = useGetUserChildQuery();
    const [addChildByID, {isError, isSuccess}] = useFindChildOnIDMutation();
    // const [idChild, setIdChild] = useState('');
    const [disabled, setDisabled] = useState(false);
    const [invisibleErrorMessage, setInvisibleErrorMessage] = useState(true);
    const {
        handleSubmit,
        control,
        reset,
        formState: {errors}
    } = useForm<idChildData>({
        mode: 'onChange'
    });

    const handleAddChildByID = (data: any): any => {
        console.log(data?.childId + ' 1');
        if (data) {
            addChildByID({childId: data?.childId}).unwrap()
        }

        console.log(data?.childId + ' 2');
    }

    const closeModal = (): any => {
        magicModal.hide();
        setInvisibleErrorMessage(true)
    }

    if (isSuccess) {
        closeModal();
    }

    if (isError) {
        setInvisibleErrorMessage(false)
        setDisabled(true)
    }

    const styles = createStyle(props);
    const ConfirmationModal = () => (
        <ModalFeature
            headerModalTitle={'Добавить ребёнка'}
            functionButton={() => handleSubmit(handleAddChildByID)}
            disabledButton={disabled}
            clickExit={() => closeModal()}>
            <View style={styles.content}>
                <Text style={styles.contentTitle}>
                    Идентификатор, выданный в школе
                </Text>
                <ControlledInputField
                    key={INPUT_DATA.name}
                    control={control}
                    errors={errors}
                    data={INPUT_DATA}
                    style={styles.inputField}
                />
                <ErrorMessage
                    displayErrorMessage={invisibleErrorMessage}
                    textMessage={'Индентификатора не существует'}/>
            </View>
        </ModalFeature>
    );

    const handleAddChild = () => {
        reset();
        return magicModal.show(ConfirmationModal);
    };

    return (
        <>{userChild !== undefined
            ? <>
            </>
            : <EmojiTextFeature
                imageEmoji={require('../../../5_features/emoji-text-feature/images/angelAmoji.png')}
                subEmojiTitle={SUB_EMOJI_TITLE}>
                <ButtonPrimary
                    title={'Добавить ребёнка'}
                    onPress={handleAddChild}
                    backgroundColor={'#EC662A'}
                    textColor={'#FFFFFF'}
                    borderRadius={10}/>
                <MagicModalPortal/>
            </EmojiTextFeature>}
        </>
    );
}
