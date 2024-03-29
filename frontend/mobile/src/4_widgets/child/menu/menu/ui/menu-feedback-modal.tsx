import {FeedbackFormData, ModalMenuFeedback} from '../../../../../5_features/modal-menu-feedback';
import {MenuFeedbackModalProps} from '../model/props';
import {useCreateFeedbackMutation} from '../../../../../6_entities/feedback';
import {SuccessFeedback} from './success-feedback';

export function MenuFeedbackModal(props: MenuFeedbackModalProps) {
  const [createFeedback, {isSuccess}] = useCreateFeedbackMutation();

  const sendFeedback = async (currentData: FeedbackFormData) => {
    await createFeedback({
      canteenId: props.canteenId,
      ...currentData
    });
  };

  return (
    <ModalMenuFeedback
      title={'Отзыв о столовой'}
      buttonTitle={'Отправить отзыв'}
      onSubmit={sendFeedback}
      successfulSubmission={isSuccess}
      successComponent={<SuccessFeedback/>}
      canteenId={props.canteenId}/>
  );
}
