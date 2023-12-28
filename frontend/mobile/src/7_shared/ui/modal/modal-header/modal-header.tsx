import {Image, Text, TouchableOpacity} from 'react-native';
import {ModalHeaderProps} from './props';
import {createStyle} from './style';
import {PaddingArea} from '../../styling/padding-area';
import {PADDINGS_HEADER} from './config';

export function ModalHeader(props: ModalHeaderProps) {
  const styles = createStyle();

  return (
    <PaddingArea
      style={styles.headerContent}
      {...PADDINGS_HEADER}>
      <Text style={styles.headerTitle}>{props.headerModalTitle}</Text>
      {
        (props.showCloseButton ?? true) && (
          <TouchableOpacity
            style={styles.image}
            onPress={props?.clickExit}>
            <Image onAccessibilityTap={props?.clickExit}
              source={require('../../../../7_shared/assets/images/exit.png')}/>
          </TouchableOpacity>
        )
      }
    </PaddingArea>
  );
}
