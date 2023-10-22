import {ModalProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area';
import {PADDINGS} from '../config/config';
import {KeyboardAvoidingView, TouchableOpacity, View} from 'react-native';
import {ModalHeader} from '../../../6_entities/modal/ui/modal-header/modal-header';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';

export function ModalFeature(props: ModalProps) {
  const styles = createStyle(props);

  return (
    <KeyboardAvoidingView style={styles.container}
      behavior="padding">
      <View style={styles.containerContent}>
        <PaddingArea
          {...PADDINGS}>
          <ModalHeader
            headerModalTitle={props.headerModalTitle}
            clickExit={props.clickExit}/>
          {props.children}
          <MarginArea marginHorizontal={32}>
            <ButtonPrimary
              title={props.buttonTitle ? props.buttonTitle : 'Сохранить изменения'}
              onPress={props.functionButton}
              backgroundColor={'#EC662A'}
              disabled={props.disabledButton}
              textColor={'#FFFFFF'}
              borderRadius={10}/>
          </MarginArea>
        </PaddingArea>
      </View>
    </KeyboardAvoidingView>
  );
}
