import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';
import {Calendar, PeriodDateBadge} from '../../../7_shared/ui/special/calendar';
import {useState} from 'react';
import {View} from 'react-native';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {createStyles} from '../consts/modal-styles';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {ModalMealPeriodProps} from '../model/props';

export function ModalMealPeriod(props: ModalMealPeriodProps) {
  const styles = createStyles();

  const [startingDate, setStartingDate] = useState(new Date());
  const [endingDate, setEndingDate] = useState(new Date());

  const onPeriodChange = (startingDate: Date, endingDate: Date) => {
    setStartingDate(startingDate);
    setEndingDate(endingDate);
  };

  return (
    <ModalWindow
      headerModalTitle={'Снять с питания'}
      clickExit={props.onClose}>
      <Calendar
        initialDate={props.initialDate}
        onPeriodChange={onPeriodChange}/>
      <MarginArea
        marginBottom={24}>
        <PeriodDateBadge
          startingDate={startingDate}
          endingDate={endingDate}/>
      </MarginArea>
      <View
        style={styles.buttons}>
        <ButtonPrimary
          flex={1}
          title={'Применить'}
          onPress={() => {
            props.onConfirm(startingDate, endingDate);
          }}/>
        <ButtonPrimary
          flex={1}
          textColor={'#2C2C2C'}
          backgroundColor={'#F7F7F7'}
          title={'Отмена'}
          onPress={props.onClose}/>
      </View>
    </ModalWindow>
  );
}
