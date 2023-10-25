import {Image, Text} from 'react-native';
import {ChildCardHeaderProps} from './props';
import {createStyle} from './style';
import {PaddingArea} from '../../../../7_shared/ui/styling/padding-area';
import {PADDINGS_HEADER} from './config';

export function ChildCardHeader(props: ChildCardHeaderProps) {
  const styles = createStyle();

  return (
    <PaddingArea
      style={styles.headerContent}
      {...PADDINGS_HEADER}>
      <Text
        style={styles.headerTitle}
        numberOfLines={1}
        ellipsizeMode={'tail'}>{props.ChildCardHeaderTitle}</Text>
      <Image style={styles.imageArrow} source={require('../../../../7_shared/assets/images/navigate-arrow.png')}/>
    </PaddingArea>
  );
}
