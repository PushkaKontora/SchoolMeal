import {magicModal} from 'react-native-magic-modal';
import {ConfirmModal} from '../ui/confirm-modal';

export function showModal(onConfirm: () => {}, onClose: () => {}) {
  magicModal.show(() => (
    <ConfirmModal
      onConfirm={onConfirm}
      onClose={onClose}/>
  ));
}

export function hideModal() {
  magicModal.hide();
}
