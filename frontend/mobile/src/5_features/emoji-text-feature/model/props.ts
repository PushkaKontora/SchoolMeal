import {PropsWithChildren} from 'react';
import {ImageSourcePropType} from 'react-native';
import {PaddingAreaProps} from '../../../7_shared/ui/styling/padding-area';

export type EmojiTextProps = {
  imageEmoji?: ImageSourcePropType,
  svgComponent?: JSX.Element,
  subEmojiTitle: string,
  gap?: number,
  paddings?: PaddingAreaProps
} & PropsWithChildren;
