import {PupilNutritionInfo} from '../../../../7_shared/model/nutrition';

export type PanelContentProps = {
  emojiImage: any,
  subEmojiTitle: string,
  visibleButton?: boolean,
  buttonTitle: string,
  onButtonPress: () => void
}

export type NutritionPanelProps = {
  pupilId: string,
  nutritionInfo: PupilNutritionInfo,
  cancelNutrition: () => void,
  resumeNutrition: () => void,
  selectedDate: Date,
  onSelectedDateChange?: (selectedDate: Date) => void
}

export type ConfirmModalProps = {
  onConfirm: () => void,
  onClose: () => void
}
