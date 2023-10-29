import {Text, View } from 'react-native';
import {ControlledInputField} from '../../../6_entities/controlled/controlled-input-field';
import {INPUT_DATA} from '../consts/input-data';
import {ErrorMessage} from '../../../6_entities/modal/ui/error-message/error-message';
import {ModalFeature} from '../../../5_features/modal-feature/ui/modal-feature';
import {ConfirmationModalProps} from '../model/props';

export function ConfirmationModal(props: ConfirmationModalProps) {
  return (
    <ModalFeature
      headerModalTitle={'Добавить ребёнка'}
      buttonTitle={'Добавить ребёнка'}
      functionButton={props.onConfirm}
      disabledButton={props.confirmDisabled}
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
        <ErrorMessage
          displayErrorMessage={props.displayError}
          textMessage={'Индентификатора не существует'}/>
      </View>
    </ModalFeature>
  );
}
