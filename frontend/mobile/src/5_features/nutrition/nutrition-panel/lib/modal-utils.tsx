import {magicModal} from 'react-native-magic-modal';
import {ConfirmationModal} from '../ui/confirmation-modal';

export function showModal(onConfirm: () => void, onClose: () => void) {
  magicModal.show(() => (
    <ConfirmationModal
      onConfirm={onConfirm}
      onClose={onClose}/>
  ));
}

export function hideModal() {
  magicModal.hide();
}
