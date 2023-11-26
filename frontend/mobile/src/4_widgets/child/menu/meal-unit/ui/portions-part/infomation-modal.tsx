import {ContentInformationModal} from '../content-information-modal/content-information-modal';
import {View} from 'react-native';
import {InformationModalProps} from './props';
import {ModalHeader} from '../../../../../../7_shared/ui/modal/modal-header/modal-header';

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
