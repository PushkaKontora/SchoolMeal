import {ModalFeature} from '../../../modal-feature/ui/modal-feature';
import {ConfirmModalProps} from '../types/props';
import {Text, View} from 'react-native';
import {modalStyles} from '../consts/styles';

export function ConfirmModal(props: ConfirmModalProps) {
  return (
    <ModalFeature
      headerModalTitle={'Снять с питания'}
      functionButton={props.onConfirm}
      clickExit={props.onClose}
      disabledButton={false}
      buttonTitle={'Снять с питания'}>
      <View
        style={modalStyles.container}>
        <Text
          style={modalStyles.title}>
          {
            'Вы уверены, что хотите снять ребёнка с питания в этот день?'
          }
        </Text>
      </View>
    </ModalFeature>
  );
}
