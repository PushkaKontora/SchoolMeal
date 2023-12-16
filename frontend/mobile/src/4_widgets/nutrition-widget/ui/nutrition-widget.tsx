import {ScrollView, View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/props';
import {useEffect, useState} from 'react';
import {isEnoughMealAmountToShow, isFeeding} from '../lib/utils';
import {
  useCancelNutritionMutation,
  useChangeNutritionPlanMutation,
  useGetPupilNutritionQuery, useResumeNutritionMutation
} from '../../../5_features/nutrition/api';
import {NutritionPlan} from '../../../7_shared/model/nutrition';
import {hideModal, showModal} from '../lib/cancellation-modal-utils';
import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import {DEFAULT_DATE} from '../../../7_shared/consts/default_date';

export function NutritionWidget(props: NutritionWidgetProps) {
  // === states ===
  const [selectedDate, setSelectedDate] = useState(DEFAULT_DATE);
  const [showToggles, setShowToggles] = useState(true);

  const [mealData, setMealData] = useState<NutritionPlan>({
    hasBreakfast: false,
    hasDinner: false,
    hasSnacks: false
  });
  const [feeding, setFeeding] = useState(isFeeding(mealData));

  // === variables ===

  const [cancelNutrition, {isSuccess: isCanceledSuccess, data: cancelData}]
    = useCancelNutritionMutation();
  const [resumeNutrition, {isSuccess: isResumedSuccess, data: resumeData}]
    = useResumeNutritionMutation();

  const [changeMeal] = useChangeNutritionPlanMutation();
  const {data: nutritionInfo, refetch: refetchNutritionInfo, isSuccess: isNutritionSuccess}
    = useGetPupilNutritionQuery(props.pupilId);

  // === useEffects ===

  useEffect(() => {
    refetchNutritionInfo();
  }, [props.pupilId]);

  useEffect(() => {
    init();
  }, [nutritionInfo]);

  useEffect(() => {
    setFeeding(isFeeding(mealData));
  }, [mealData]);

  useEffect(() => {
    setShowToggles(feeding && isEnoughMealAmountToShow(mealData));
  }, [feeding, mealData]);

  useEffect(() => {
    if (isCanceledSuccess) {
      nutritionInfo.cancellationPeriods = cancelData;
    }
  }, [isCanceledSuccess]);

  useEffect(() => {
    if (isResumedSuccess) {
      nutritionInfo.cancellationPeriods = resumeData;
      console.log(resumeData);
    }
  }, [isResumedSuccess]);

  // === functions ===

  const dateToString = (date: Date) => {
    return dateToISOWithoutTime(date);
  };

  const init = () => {
    if (isNutritionSuccess) {
      const newMealData = {
        hasBreakfast: nutritionInfo.mealPlan.hasBreakfast,
        hasDinner: nutritionInfo.mealPlan.hasDinner,
        hasSnacks: nutritionInfo.mealPlan.hasSnacks
      };

      setMealData(newMealData);
    }
  };

  const onCheckChange = async (changedProperties: Partial<NutritionPlan>) => {
    if (nutritionInfo) {
      const newMealData = {
        ...mealData,
        ...changedProperties
      };

      await changeMeal({
        pupilId: props.pupilId,
        body: newMealData
      });

      setMealData(newMealData);
    }
  };

  const onHeaderCheckChange = async (turnedOn: boolean) => {
    await onCheckChange({
      hasBreakfast: turnedOn,
      hasDinner: turnedOn,
      hasSnacks: turnedOn
    });
  };

  const showCancellationModal = () => showModal(selectedDate, {
    onConfirm: async (startingDate, endingDate) => {
      await cancelNutrition({
        pupilId: props.pupilId,
        body: {
          startsAt: dateToString(startingDate),
          endsAt: dateToString(endingDate),
          reason: 'Я заболел филлеро-вирусом'
        }
      });
      hideModal();
    },
    onClose: () => {
      hideModal();
    }
  });

  // === render ===

  return (
    <ScrollView>
      <View
        style={styles.background}>
        <View
          style={styles.card}>

          <NutritionHeaderFeature
            nutritionInfo={nutritionInfo}
            onToggle={(toggledRight: boolean) => onHeaderCheckChange(toggledRight)}
            defaultToggleState={feeding}/>

          <NutritionCertFeature
            nutritionInfo={nutritionInfo}/>

          {
            showToggles &&
            <NutritionTogglesFeature
              onToggleBreakfast={(turnedOn: boolean) => {
                onCheckChange({hasBreakfast: turnedOn});
              }}
              onToggleLunch={(turnedOn: boolean) => {
                onCheckChange({hasDinner: turnedOn});
              }}
              onToggleAfternoonSnack={(turnedOn: boolean) => {
                onCheckChange({hasSnacks: turnedOn});
              }}
              breakfastState={mealData?.hasBreakfast}
              lunchState={mealData?.hasDinner}
              afternoonSnackState={mealData?.hasSnacks}
              hasBreakfast={true}
              hasLunch={true}
              hasAfternoonSnack={true}/>
          }

          {
            feeding &&
            <NutritionPanel
              refetchNutritionInfo={refetchNutritionInfo}
              nutritionInfo={nutritionInfo}
              pupilId={props.pupilId}
              selectedDate={selectedDate}
              onSelectedDateChange={setSelectedDate}
              cancelNutrition={showCancellationModal}
              resumeNutrition={async () => {
                await resumeNutrition({
                  pupilId: props.pupilId,
                  body: {
                    date: dateToString(selectedDate)
                  }
                });
              }}/>
          }

        </View>
      </View>
    </ScrollView>
  );
}
