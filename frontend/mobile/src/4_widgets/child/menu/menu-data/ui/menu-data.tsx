import {MenuDataProps} from '../model/props';
import {View} from 'react-native';
import {createStyle} from '../consts/style';
import {TitleText} from '../../../../../7_shared/ui/text/title-text/title.text';
import {MiniCalendar} from '../../../../../7_shared/ui/special/mini-calendar';
import {setDataMenu} from '../../menu/model/menu-slice/menu-slice';
import {useAppDispatch, useAppSelector} from '../../../../../../store/hooks';
import {dateToISOWithoutTime} from '../../../../../6_entities/date/lib/utils';
import {MonthPicker} from '../../../../../7_shared/ui/special/mini-calendar/ui/month-picker';
import {useEffect} from 'react';

export function MenuData(props: MenuDataProps) {
  const styles = createStyle(props);
  const dispatch = useAppDispatch();
  const now = new Date();

  const handlerClickDate = (date: any) => {
    dispatch(setDataMenu(dateToISOWithoutTime(date)));
    console.log(dateToISOWithoutTime(date), 'MenuData');
  };

  const handlerMonth = () => {
  };

  return (
    <View style={styles.container}>
      <View style={styles.menuTitle}>
        <TitleText title={'Меню'}
          paddingBottom={0}/>
        <MonthPicker date={now} onMonthChange={handlerMonth}/>
      </View>
      <MiniCalendar selectionColor={'#E9632C'}
        onDateChange={handlerClickDate}/>
    </View>
  );
}
