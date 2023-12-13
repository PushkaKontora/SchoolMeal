import {Text, View} from 'react-native';
import {styles} from '../consts/styles';
import {MiniCalendar} from '../../../../7_shared/ui/special/mini-calendar';
import {DEFAULT_ITEM_NUMBER, PANELS, SELECTION_COLOR} from '../config/config';
import {useEffect, useState} from 'react';
import {NutritionPanelProps} from '../types/props';
import {PanelPressListeners} from '../types/types';
import {isDateExpired} from '../lib/date-utils';
import {hideModal, showModal} from '../lib/modal-utils';
import {createPanels} from '../lib/create-panels';
import {MonthPicker} from '../../../../7_shared/ui/special/mini-calendar/ui/month-picker';
import {findFirstFullWeek} from '../../../../7_shared/ui/special/mini-calendar/lib/dates-utils';
import {DEFAULT_DATE} from '../../../../7_shared/consts/default_date';
import {dateToISOWithoutTime} from '../../../../7_shared/lib/date';
import {useCancelNutritionMutation, useResumeNutritionMutation} from '../../api';
import { isNutritionCancelled} from '../lib/period-utils';

export function NutritionPanel(props: NutritionPanelProps) {
  const [selectedDate, setSelectedDate] = useState<Date>(DEFAULT_DATE);
  const [monthDate, setMonthDate] = useState<Date>(DEFAULT_DATE);
  const [cancelledCurrentNutrition, setCancelledCurrentNutrition]
    = useState<boolean | undefined>(undefined);

  const [cancelNutrition, {isSuccess: isCanceledSuccess}] = useCancelNutritionMutation();
  const [resumeNutrition, {isSuccess: isResumedSuccess}] = useResumeNutritionMutation();

  const dateToString = (date: Date) => {
    return dateToISOWithoutTime(date);
  };

  const showModalCustom = () => showModal(
    async () => {
      await cancelNutrition({
        pupilId: props.pupilId,
        body: {
          startsAt: dateToString(selectedDate),
          endsAt: dateToString(selectedDate),
          reason: 'Я заболел филлеро-вирусом'
        }
      });
      hideModal();
    },
    () => {
      hideModal();
    });

  useEffect(() => {
    setCancelledCurrentNutrition(
      isNutritionCancelled(dateToString(selectedDate), props.nutritionInfo.cancellationPeriods)
    );
  }, [selectedDate,
    props.nutritionInfo,
    props.nutritionInfo.cancellationPeriods]);

  useEffect(() => {
    if (isCanceledSuccess) {
      props.refetchNutritionInfo();
    }
  }, [isCanceledSuccess]);

  useEffect(() => {
    if (isResumedSuccess) {
      props.refetchNutritionInfo();
    }
  }, [isResumedSuccess]);

  const panelListeners: PanelPressListeners = {
    onCancel: showModalCustom,
    onSubmit: async () => {
      if (cancelledCurrentNutrition) {
        await resumeNutrition({
          pupilId: props.pupilId,
          body: {
            date: dateToString(selectedDate)
          }
        });
      }
    }
  };

  const panels = createPanels(PANELS, panelListeners);

  const onDateChange = (date: Date) => {
    setSelectedDate(date);
    setMonthDate(date);
  };

  const onMonthChange = (date: Date) => {
    setMonthDate(date);
    setSelectedDate(findFirstFullWeek(date));
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
          currentDate={selectedDate}
          onDateChange={onDateChange}/>
      </View>

      {
        cancelledCurrentNutrition
          ? panels.canceled({visibleButton: !isDateExpired(selectedDate)})
          : panels.submitted({visibleButton: !isDateExpired(selectedDate)})
      }

    </View>
  );
}
