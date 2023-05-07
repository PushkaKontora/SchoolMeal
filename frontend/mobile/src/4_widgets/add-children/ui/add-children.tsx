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


export function AddChildrenWidget(props: ModalAddChildProps) {
    const {data: userChild} = useGetUserChildQuery();
    const [addChildByID, {isError, isSuccess}] = useFindChildOnIDMutation();
    // const [idChild, setIdChild] = useState('');
    const [disabled, setDisabled] = useState(false);
    const [invisibleErrorMessage, setInvisibleErrorMessage] = useState(true);
    const {
        handleSubmit,
        control,
        formState: {errors}
    } = useForm<idChildData>({
        mode: 'onChange'
    });
    const item = {
        name: 'idChild',
        label: 'id',
        type: '',
        options: {
            required: 'Вы не заполнили это поле'
        },
        placeholder: ''
    };

    const handleAddChildByID = (data: idChildData) => {
        if (data) {
            addChildByID({childId: data.idChild}).unwrap()
        }
        console.log(data);
    }

    if (isSuccess) {
        setInvisibleErrorMessage(true)

        magicModal.hide().then(r => console.log('modal close'));
    }

    if (isError) {
        setInvisibleErrorMessage(false)
        setDisabled(true)
    }
//todo: сделать очищение поля при закрытии модалки

    const styles = createStyle(props);
    const ConfirmationModal = () => (
        <ModalFeature
            headerModalTitle={'Добавить ребёнка'}
            functionButton={() => handleSubmit(handleAddChildByID)}
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
