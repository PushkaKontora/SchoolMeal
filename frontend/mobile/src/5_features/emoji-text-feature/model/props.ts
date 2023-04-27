import {PropsWithChildren} from 'react';
import {ImageSourcePropType} from 'react-native';

export type EmojiTextProps = {
  imageEmoji: any,
  subEmojiTitle: string
} & PropsWithChildren;
