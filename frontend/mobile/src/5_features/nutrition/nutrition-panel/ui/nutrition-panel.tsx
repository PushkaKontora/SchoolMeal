import {Text, View} from 'react-native';
import {styles} from '../consts/styles';
import {MiniCalendar} from '../../../../7_shared/ui/special/mini-calendar';
import {DEFAULT_ITEM_NUMBER, PANELS, SELECTION_COLOR} from '../config/config';
import {useEffect, useState} from 'react';
import {NutritionPanelProps} from '../types/props';
import {PanelPressListeners} from '../types/types';
import {isDateExpired} from '../lib/date-utils';
import {createPanels} from '../lib/create-panels';
import {MonthPicker} from '../../../../7_shared/ui/special/mini-calendar/ui/month-picker';
import {findFirstFullWeek} from '../../../../7_shared/ui/special/mini-calendar/lib/dates-utils';
import {dateToISOWithoutTime} from '../../../../7_shared/lib/date';
import { isNutritionCancelled} from '../lib/period-utils';

export function NutritionPanel(props: NutritionPanelProps) {
  const [monthDate, setMonthDate]
    = useState<Date>(props.selectedDate);
  const [cancelledCurrentNutrition, setCancelledCurrentNutrition]
    = useState<boolean | undefined>(undefined);

  const dateToString = (date: Date) => {
    return dateToISOWithoutTime(date);
  };

  useEffect(() => {
    setCancelledCurrentNutrition(
      isNutritionCancelled(dateToString(props.selectedDate), props.nutritionInfo.cancellationPeriods)
    );
  }, [props.selectedDate,
    props.nutritionInfo,
    props.nutritionInfo.cancellationPeriods]);

  const panelListeners: PanelPressListeners = {
    onCancel: props.cancelNutrition,
    onSubmit: () => {
      if (cancelledCurrentNutrition) {
        props.resumeNutrition();
      }
    }
  };

  const panels = createPanels(PANELS, panelListeners);

  const onDateChange = (date: Date) => {
    setMonthDate(date);

    if (props.onSelectedDateChange) {
      props.onSelectedDateChange(date);
    }
  };

  const onMonthChange = (date: Date) => {
    setMonthDate(date);

    if (props.onSelectedDateChange) {
      props.onSelectedDateChange(findFirstFullWeek(date));
    }
  };

  return (
    <View
      style={styles.container}>
      <Text
        style={styles.title}>
        {'Снять с питания'}
      </Text>

      <Text
        style={styles.description}>
        {'Выберите дни, когда ребенка не будет в школе (не будет питаться)'}
      </Text>

      <View
        style={styles.monthPicker}>
        <MonthPicker
          date={monthDate}
          onMonthChange={onMonthChange}/>
      </View>

      <View
        style={styles.calendar}>
        <MiniCalendar
          selectionColor={SELECTION_COLOR}
          itemNumber={DEFAULT_ITEM_NUMBER}
          currentDate={props.selectedDate}
          onDateChange={onDateChange}/>
      </View>

      {
        cancelledCurrentNutrition
          ? panels.canceled({visibleButton: !isDateExpired(props.selectedDate)})
          : panels.submitted({visibleButton: !isDateExpired(props.selectedDate)})
      }

    </View>
  );
}
