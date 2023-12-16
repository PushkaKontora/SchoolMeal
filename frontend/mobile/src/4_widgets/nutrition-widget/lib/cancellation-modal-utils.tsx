import {magicModal} from 'react-native-magic-modal';
import {ModalMealPeriod} from '../../../5_features/modal-meal-period';
import {ModalMealPeriodProps} from '../../../5_features/modal-meal-period';

export function showModal(selectedDate: Date, props: ModalMealPeriodProps) {
  magicModal.show(() => (
    <ModalMealPeriod
      initialDate={selectedDate}
      {...props}/>
  ));
}

export function hideModal() {
  magicModal.hide();
}
