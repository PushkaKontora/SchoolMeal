import {magicModal} from 'react-native-magic-modal';
import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';
import {FeedbackForm} from '../../../6_entities/feedback/ui/feedback-form';
import {FeedbackModalProps} from '../model/props';
import {useEffect} from 'react';
import {CLOSE_AFTER_MS} from '../const/config';

export function ModalWithLimitedField(props: FeedbackModalProps) {
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
      headerModalTitle={props.title}
      clickExit={closeModal}>
      {
        props.successfulSubmission ? (
          props.successComponent
        ) : (
          <FeedbackForm
            canteenId={props.canteenId}
            symbolLimit={props.symbolLimit}
            buttonTitle={props.buttonTitle}
            onSubmit={props.onSubmit}/>
        )
      }
    </ModalWindow>
  );
}
