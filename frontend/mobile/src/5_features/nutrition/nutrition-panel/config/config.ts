import {PanelConfig} from '../types/types';

export const SELECTION_COLOR = '#EE6725';
export const DEFAULT_ITEM_NUMBER = 5;

export function GET_LIMIT_TIME_TO_CANCEL_NUTRITION_FOR_TOMORROW() {
  const now = new Date(Date.now());
  now.setHours(15, 0, 0, 0);
  return now;
}

export const PANELS: PanelConfig = {
  submitted: {
    emojiImage: require('../../../emoji-text-feature/images/happy_emoji.png'),
    subEmojiTitle: 'Ваш ребенок питается в этот день',
    buttonTitle: 'Снять с питания'
  },
  canceled: {
    emojiImage: require('../../../emoji-text-feature/images/frustrated_emoji.png'),
    subEmojiTitle: 'Ваш ребенок снят с питания в этот день',
    buttonTitle: 'Поставить на питание'
  }
};
