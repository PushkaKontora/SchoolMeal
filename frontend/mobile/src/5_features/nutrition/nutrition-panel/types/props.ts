import {Child} from '../../../../6_entities/child/model/child';

export type PanelContentProps = {
  emojiImage: any,
  subEmojiTitle: string,
  buttonTitle: string,
  onButtonPress: () => void
}

export type NutritionPanelProps = {
  child?: Child,
  refetchChild: () => void
}

export type ConfirmModalProps = {
  onConfirm: () => {},
  onClose: () => {}
}
