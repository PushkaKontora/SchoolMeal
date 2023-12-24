import {magicModal} from 'react-native-magic-modal';
import {ModalMealPeriod} from '../../../5_features/modal-meal-period';
import {ModalMealPeriodProps} from '../../../5_features/modal-meal-period';
import {CommentFormData, ModalNutritionComment} from '../../../5_features/modal-nutrition-comment';
import {ModalNutritionCommentProps} from '../../../5_features/modal-nutrition-comment';
import {dateToString} from './date-utils';
import {CancelNutritionIn} from '../../../5_features/nutrition/api/types';

export function createPeriodModal(selectedDate: Date, props: ModalMealPeriodProps) {
  return (
    <ModalMealPeriod
      initialDate={selectedDate}
      {...props}/>
  );
}

export function createCommentModal(props: ModalNutritionCommentProps) {
  return (
    <ModalNutritionComment
      {...props}/>
  );
}

export function createCancellationModal(
  sendCancellation: (body: CancelNutritionIn['body']) => Promise<void>) {
  const showCancellationModal = (selectedDate: Date) => {
    magicModal.show(() => createPeriodModal(selectedDate, {
      onConfirm: showCommentModal,
      onClose: () => {
        hideModal();
      }
    }));
  };

  const showCommentModal = async (startingDate: Date, endingDate: Date) => {
    await hideModal();
    magicModal.show(() => createCommentModal({
      onSendClick: async (commentData: CommentFormData) => {
        await sendCancellation({
          startsAt: dateToString(startingDate),
          endsAt: dateToString(endingDate),
          reason: commentData.reason
        });
        await hideModal();
      }
    }));
  };

  return showCancellationModal;
}

export function hideModal() {
  return magicModal.hide();
}
