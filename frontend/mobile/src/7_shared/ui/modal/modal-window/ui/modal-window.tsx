import {ModalProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PADDINGS} from '../config/config';
import {KeyboardAvoidingView, View} from 'react-native';
import {ModalHeader} from '../../modal-header/modal-header';
import {PaddingArea} from '../../../styling/padding-area';

export function ModalWindow(props: ModalProps) {
  const styles = createStyle();

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior="padding">
      <View style={styles.containerContent}>
        <ModalHeader
          headerModalTitle={props.headerModalTitle}
          clickExit={props.clickExit}
          showCloseButton={props.showCloseButton}/>
        <PaddingArea
          {...PADDINGS}>
          {props.children}
        </PaddingArea>
      </View>
    </KeyboardAvoidingView>
  );
}
