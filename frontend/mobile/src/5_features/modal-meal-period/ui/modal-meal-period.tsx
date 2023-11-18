import {magicModal} from 'react-native-magic-modal';
import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';
import {Calendar} from '../../../7_shared/ui/special/calendar';

export function ModalMealPeriod() {
  const closeModal = () => {
    magicModal.hide();
  };

  return (
    <ModalWindow
      headerModalTitle={'Снять с питания'}
      clickExit={closeModal}>
      <Calendar/>
    </ModalWindow>
  );
}
