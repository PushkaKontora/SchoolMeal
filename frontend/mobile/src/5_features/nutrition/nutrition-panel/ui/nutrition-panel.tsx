import {Text, View} from 'react-native';
import {styles} from '../consts/styles';
import {MiniCalendar} from '../../../../7_shared/ui/special/mini-calendar';
import {DEFAULT_DATE, DEFAULT_ITEM_NUMBER, PANELS, SELECTION_COLOR} from '../config/config';
import {useEffect, useState} from 'react';
import {NutritionPanelProps} from '../types/props';
import {createPanels} from '../lib/panel-utils';
import {PanelPressListeners} from '../types/types';
import {useCancelMealMutation} from '../../../../6_entities/meal/api/api';
import {CancelMealPeriods} from '../../../../7_shared/model/cancelMealPeriods';
import {findPeriodIdByDate} from '../lib/meal-utils';

export function NutritionPanel(props: NutritionPanelProps) {
  const [selectedDate, setSelectedDate] = useState<Date>(DEFAULT_DATE);
  const [currentCancelMeal, setCurrentCancelMeal] = useState<CancelMealPeriods | undefined>(undefined);

  const [cancelMeal, {isSuccess: canceledSuccess}] = useCancelMealMutation();
  const [deleteCanceledMeal, {isSuccess: deletedSuccess}] = useCancelMealMutation();

  useEffect(() => {
    if (props.child && selectedDate) {
      setCurrentCancelMeal(
        findPeriodIdByDate(props.child.cancelMealPeriods, selectedDate)
      );
    }
  }, [props.child]);

  useEffect(() => {
    if (canceledSuccess) {
      props.refetchChild();
    }
  }, [canceledSuccess]);

  useEffect(() => {
    if (deletedSuccess) {
      props.refetchChild();
    }
  }, [deletedSuccess]);

  const panelListeners: PanelPressListeners = {
    onRegister: async () => {
      await cancelMeal({
        pupilId: props?.child?.id,
        startDate: selectedDate
      });
    },
    onDeregister: async () => {
      if (currentCancelMeal) {
        await deleteCanceledMeal(currentCancelMeal.pupilId);
      }
    }
  };

  const panels = createPanels(PANELS, panelListeners);

  const onDateChange = (date: Date) => {
    setSelectedDate(date);
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
      
      <MiniCalendar
        selectionColor={SELECTION_COLOR}
        itemNumber={DEFAULT_ITEM_NUMBER}
        currentDate={selectedDate}
        onDateChange={onDateChange}/>

      {
        currentCancelMeal
          ? panels.deregister
          : panels.register
      }

    </View>
  );
}
