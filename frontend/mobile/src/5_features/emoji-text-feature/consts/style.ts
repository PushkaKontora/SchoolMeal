import {StyleSheet} from 'react-native';
import {EmojiTextProps} from '../model/props';
import {DEFAULT_GAP} from '../config/config';

export const createStyle = (props: EmojiTextProps) => StyleSheet.create({
  titles: {
    flexDirection: 'column',
    alignItems: 'center',
    gap: props.gap || DEFAULT_GAP
  },
  subEmoji: {
    fontWeight: '500',
    fontSize: 16,
    color: '#B1B1B1',
    lineHeight: 22.4,
    textAlign: 'center',
  },
  image: {
    width: 54,
    height: 54
  }
});
