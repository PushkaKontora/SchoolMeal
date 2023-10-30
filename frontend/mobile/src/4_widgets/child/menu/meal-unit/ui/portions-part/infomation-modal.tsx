import {ModalHeader} from '../../../../../../6_entities/modal/ui/modal-header/modal-header';
import {ContentInformationModal} from '../content-information-modal/content-information-modal';
import {View} from 'react-native';
import {InformationModalProps} from './props';

export function InformationModal(props: InformationModalProps) {
  return (
    <View style={props.styles.containerModal}>
      <ModalHeader
        headerModalTitle={props.portions.food.name}
        clickExit={props.onExit}/>
      <ContentInformationModal imagePath={props.imagePath} portions={props.portions}/>
    </View>
  );
}
