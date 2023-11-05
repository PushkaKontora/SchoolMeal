import {ConfirmModalProps} from '../types/props';
import {Text, View} from 'react-native';
import {modalStyles} from '../consts/styles';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';
import {ModalWindow} from '../../../../7_shared/ui/modal/modal-window/ui/modal-window';

export function ConfirmationModal(props: ConfirmModalProps) {
  return (
    <ModalWindow
      headerModalTitle={'Снять с питания'}
      clickExit={props.onClose}>
      <View
        style={modalStyles.container}>
        <Text
          style={modalStyles.title}>
          {
            'Вы уверены, что хотите снять ребёнка с питания в этот день?'
          }
        </Text>
        <ButtonPrimary
          title={'Снять с питания'}
          onPress={props.onConfirm}
          backgroundColor={'#EC662A'}
          textColor={'#FFFFFF'}
          borderRadius={10}/>
      </View>
    </ModalWindow>
  );
}
