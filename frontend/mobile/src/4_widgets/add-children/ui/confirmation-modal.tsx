import {Text, View } from 'react-native';
import {ControlledInputField} from '../../../7_shared/ui/controlled/controlled-input-field';
import {INPUT_DATA} from '../consts/input-data';
import {TextErrorMessage} from '../../../7_shared/ui/special/error-message/text-error-message';
import {ConfirmationModalProps} from '../model/props';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';

export function ConfirmationModal(props: ConfirmationModalProps) {
  return (
    <ModalWindow
      headerModalTitle={'Добавить ребёнка'}
      clickExit={props.onClose}>
      <View style={props.styles.content}>
        <Text style={props.styles.contentTitle}>
                      Идентификатор, выданный в школе
        </Text>
        <ControlledInputField
          key={INPUT_DATA.name}
          control={props.control}
          errors={props.errors}
          data={INPUT_DATA}
          style={props.styles.inputField}
          autoFocus={true}
        />
        <TextErrorMessage
          displayErrorMessage={props.displayError}
          textMessage={'Идентификатора не существует'}/>
      </View>
      <ButtonPrimary
        title={'Добавить ребёнка'}
        onPress={props.onConfirm}
        backgroundColor={'#EC662A'}
        disabled={props.confirmDisabled}
        textColor={'#FFFFFF'}
        borderRadius={10}/>
    </ModalWindow>
  );
}
