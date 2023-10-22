import {Text, View} from 'react-native';
import {styles} from '../consts/styles';
import {MiniCalendar} from '../../../../7_shared/ui/special/mini-calendar';
import {DEFAULT_DATE, DEFAULT_ITEM_NUMBER, PANELS, SELECTION_COLOR} from '../config/config';
import {useEffect, useState} from 'react';
import {NutritionPanelProps} from '../types/props';
import {PanelPressListeners} from '../types/types';
import {CancelMealPeriods} from '../../../../7_shared/model/cancelMealPeriods';
import {findPeriodIdByDate, isDateExpired} from '../lib/meal-utils';
import {hideModal, showModal} from '../lib/modal-utils';
import {dateToISOWithoutTime} from '../../../../6_entities/date/lib/utils';
import {useDeleteCanceledMealMutation, useCancelMealMutation} from '../../../../6_entities/meal/api/api';
import {createPanels} from '../lib/create-panels';
import {MonthPicker} from '../../../../7_shared/ui/special/mini-calendar/ui/month-picker';

export function NutritionPanel(props: NutritionPanelProps) {
  const [selectedDate, setSelectedDate] = useState<Date>(DEFAULT_DATE);
  const [currentCancelMeal, setCurrentCancelMeal] = useState<CancelMealPeriods | undefined>(undefined);

  const [cancelMeal, {isSuccess: canceledSuccess}] = useCancelMealMutation();
  const [deleteCanceledMeal, {isSuccess: deletedSuccess}] = useDeleteCanceledMealMutation();

  const showModalCustom = () => showModal(
    async () => {
      await cancelMeal({
        pupilId: props?.child?.id,
        startDate: dateToISOWithoutTime(selectedDate)
      });
      hideModal();
    },
    () => {
      hideModal();
    });

  useEffect(() => {
    if (props.child && selectedDate) {
      setCurrentCancelMeal(
        findPeriodIdByDate(props.child.cancelMealPeriods, selectedDate)
      );
    }
  }, [selectedDate]);

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
    onCancel: showModalCustom,
    onSubmit: async () => {
      if (currentCancelMeal) {
        await deleteCanceledMeal(currentCancelMeal.id);
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

      <View
        style={styles.monthPicker}>
        <MonthPicker
          date={selectedDate}
          onMonthChange={onDateChange}/>
      </View>

      <View
        style={styles.calendar}>
        <MiniCalendar
          selectionColor={SELECTION_COLOR}
          itemNumber={DEFAULT_ITEM_NUMBER}
          currentDate={selectedDate}
          onDateChange={onDateChange}/>
      </View>

      {
        currentCancelMeal
          ? panels.canceled({visibleButton: !isDateExpired(selectedDate)})
          : panels.submitted({visibleButton: !isDateExpired(selectedDate)})
      }

    </View>
  );
}
