import {SUB_EMOJI_TITLE} from '../consts/consts';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {EmojiTextFeature} from '../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import {magicModal, MagicModalPortal} from 'react-native-magic-modal';
import {ModalAddChildProps} from '../model/props';
import {createStyle} from '../consts/style-modal';
import {useEffect, useState} from 'react';
import {View} from 'react-native';
import {useForm} from 'react-hook-form';
import {AddChildData} from '../types';
import {ChildCard} from '../../child/child-card/ui/child-card';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {ConfirmationModal} from './confirmation-modal';
import {useAddChildMutation, useGetChildrenQuery} from '../../../6_entities/child';
import {Child} from '../../../6_entities/child';

export function AddChildrenWidget(props: ModalAddChildProps) {
  const {data: children} = useGetChildrenQuery();
  const [addChildByID, {isError, isSuccess}] = useAddChildMutation();
  // const [idChild, setIdChild] = useState('');
  const [disabled, setDisabled] = useState(false);
  const [invisibleErrorMessage, setInvisibleErrorMessage] = useState(true);
  const {
    handleSubmit,
    control,
    reset,
    formState: {errors}
  } = useForm<AddChildData>({
    mode: 'onChange'
  });

  const handleAddChildByID = (data: AddChildData) => {
    if (data) {
      addChildByID(data.childId).unwrap();
    }
  };

  const closeModal = (): void => {
    magicModal.hide();
    setInvisibleErrorMessage(true);
    setDisabled(false);
  };

  useEffect(() => {
    if (isSuccess) {
      closeModal();
    }
  }, [isSuccess]);

  useEffect(() => {
    if (isError) {
      setInvisibleErrorMessage(false);
      setDisabled(true);
    }
  }, [isError]);

  const styles = createStyle();

  const handleAddChild = () => {
    reset();
    return magicModal.show(() => (
      <ConfirmationModal
        onConfirm={handleSubmit(handleAddChildByID)}
        onClose={closeModal}
        confirmDisabled={disabled}
        styles={styles}
        control={control}
        errors={errors}
        displayError={invisibleErrorMessage}/>
    ));
  };

  return (
    <View style={styles.container}>
      {children && (children as Child[]).length !== 0
        ? <>
          {children ? (children as Child[]).map(child =>
            <ChildCard key={child.id}
              child={child}
              navigation={props.navigation}/>) : null}
          <MarginArea
            marginTop={16}>
            <ButtonPrimary
              title={'Добавить ребёнка'}
              onPress={handleAddChild}
              backgroundColor={'#EC662A'}
              textColor={'#FFFFFF'}
              borderRadius={10}/>
          </MarginArea>
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
        </EmojiTextFeature>}
      <MagicModalPortal/>
    </View>
  );
}
