import {magicModal} from 'react-native-magic-modal';
import {ModalMealPeriod} from '../../../5_features/modal-meal-period';
import {ModalMealPeriodProps} from '../../../5_features/modal-meal-period';
import {ModalNutritionComment} from '../../../5_features/modal-nutrition-comment';
import {ModalNutritionCommentProps} from '../../../5_features/modal-nutrition-comment';

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

export function hideModal() {
  return magicModal.hide();
}
