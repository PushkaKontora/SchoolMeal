import {EmojiTextProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: EmojiTextProps) => StyleSheet.create({
  container: {
  },
  titles: {
    flexDirection: 'column',
    gap: 6,
    alignItems: 'center',
    marginBottom: 21,
    marginHorizontal: 'auto',
  },
  subEmoji: {
    fontWeight: '400',
    fontSize: 12,
    color: '#B1B1B1',
    maxWidth: 190,
    textAlign: 'center',
  }
});
