import {ScrollView, View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/nutrition-widget-props';
import {useEffect, useState} from 'react';
import {isEnoughMealAmountToShow, isFeeding} from '../lib/nutrition-utils';
import {
  useCancelNutritionMutation,
  useChangeNutritionPlanMutation,
  useGetPupilNutritionQuery, useResumeNutritionMutation
} from '../../../5_features/nutrition/api';
import {NutritionPlan, PupilNutritionInfo} from '../../../7_shared/model/nutrition';
import {
  createCancellationModal
} from '../lib/cancellation-modal-utils';
import {DEFAULT_DATE} from '../../../7_shared/consts/default_date';
import {CancelNutritionIn} from '../../../5_features/nutrition/api/types';
import {dateToString, getLastAbleDateToCancelNutrition} from '../lib/date-utils';
import {ToastService} from '../../../7_shared/lib/toast-service';
import {CANCELLED_NUTRITION_DESCRIPTION, RESUMED_NUTRITION_DESCRIPTION} from '../consts/strings';

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

  const [nutritionInfoState, setNutritionInfoState]
    = useState<PupilNutritionInfo | undefined>(undefined);

  // === api calls ===

  const [cancelNutrition, {isSuccess: isCanceledSuccess, data: cancelData}]
    = useCancelNutritionMutation();
  const [resumeNutrition, {isSuccess: isResumedSuccess, data: resumeData}]
    = useResumeNutritionMutation();

  const [changeMeal] = useChangeNutritionPlanMutation();
  const {data: nutritionInfo,  refetch: refetchNutritionInfo, isSuccess: isNutritionSuccess}
    = useGetPupilNutritionQuery(props.pupilId);

  // === useEffects ===

  useEffect(() => {
    refetchNutritionInfo();
  }, [props.pupilId]);

  useEffect(() => {
    if (isNutritionSuccess) {
      const newMealData = {
        hasBreakfast: nutritionInfo.mealPlan.hasBreakfast,
        hasDinner: nutritionInfo.mealPlan.hasDinner,
        hasSnacks: nutritionInfo.mealPlan.hasSnacks
      };

      setMealData(newMealData);
      setNutritionInfoState(nutritionInfo as PupilNutritionInfo);
    }
  }, [nutritionInfo]);

  useEffect(() => {
    setFeeding(isFeeding(mealData));
  }, [mealData]);

  useEffect(() => {
    setShowToggles(feeding && isEnoughMealAmountToShow(mealData));
  }, [feeding, mealData]);

  useEffect(() => {
    if (isCanceledSuccess && cancelData) {
      setNutritionInfoState({
        ...nutritionInfoState,
        cancellationPeriods: cancelData
      });
      ToastService.show('success', {
        description: CANCELLED_NUTRITION_DESCRIPTION
      });
    }
  }, [isCanceledSuccess, cancelData]);

  useEffect(() => {
    if (isResumedSuccess) {
      setNutritionInfoState({
        ...nutritionInfoState,
        cancellationPeriods: resumeData
      });
      ToastService.show('success', {
        description: RESUMED_NUTRITION_DESCRIPTION
      });
    }
  }, [isResumedSuccess]);

  // === callback functions ===

  const onToggleChange = async (changedProperties: Partial<NutritionPlan>) => {
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
    await onToggleChange({
      hasBreakfast: turnedOn,
      hasDinner: turnedOn,
      hasSnacks: turnedOn
    });
  };

  // === modal functions  ===

  const sendCancellation = async (body: CancelNutritionIn['body']) => {
    await cancelNutrition({
      pupilId: props.pupilId,
      body: body
    });
  };

  const showCancellationModal = createCancellationModal(sendCancellation, getLastAbleDateToCancelNutrition);

  // === render ===

  return (
    <ScrollView>
      <View
        style={styles.background}>
        <View
          style={styles.card}>

          <NutritionHeaderFeature
            nutritionInfo={nutritionInfoState}
            onToggle={(toggledRight: boolean) => onHeaderCheckChange(toggledRight)}
            defaultToggleState={feeding}/>

          <NutritionCertFeature
            nutritionInfo={nutritionInfoState}/>

          {
            showToggles &&
            <NutritionTogglesFeature
              onToggleBreakfast={(turnedOn: boolean) => {
                onToggleChange({hasBreakfast: turnedOn});
              }}
              onToggleLunch={(turnedOn: boolean) => {
                onToggleChange({hasDinner: turnedOn});
              }}
              onToggleAfternoonSnack={(turnedOn: boolean) => {
                onToggleChange({hasSnacks: turnedOn});
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
              nutritionInfo={nutritionInfoState}
              pupilId={props.pupilId}
              selectedDate={selectedDate}
              onSelectedDateChange={setSelectedDate}
              cancelNutrition={() => showCancellationModal(selectedDate)}
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
