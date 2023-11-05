import {magicModal} from 'react-native-magic-modal';
import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';
import {ModalLimitedField} from './modal-limited-field';
import {FeedbackModalProps} from '../model/props';
import {ModalFeedbackSubmitted} from './modal-feedback-submitted';
import {useEffect} from 'react';
import {CLOSE_AFTER_MS} from '../const/config';

export function FeedbackModal(props: FeedbackModalProps) {
  const closeModal = () => {
    magicModal.hide();
  };

  useEffect(() => {
    if (props.successfulSubmission) {
      setTimeout(() => {
        closeModal();
      }, CLOSE_AFTER_MS);
    }
  }, [props.successfulSubmission]);

  return (
    <ModalWindow 
      headerModalTitle={'Отзыв о столовой'} 
      clickExit={closeModal}>
      {
        props.successfulSubmission ? (
          <ModalFeedbackSubmitted/>
        ) : (
          <ModalLimitedField
            symbolLimit={props.symbolLimit}
            buttonTitle={props.buttonTitle}
            onSubmit={() => console.log('clicked')}/>
        )
      }
    </ModalWindow>
  );
}
