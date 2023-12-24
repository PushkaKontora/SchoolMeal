import {ScrollView, View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/nutrition-widget-props';
import {useEffect, useState} from 'react';
import {isEnoughMealAmountToShow, isFeeding} from '../lib/utils';
import {
  useCancelNutritionMutation,
  useChangeNutritionPlanMutation,
  useGetPupilNutritionQuery, useResumeNutritionMutation
} from '../../../5_features/nutrition/api';
import {NutritionPlan, PupilNutritionInfo} from '../../../7_shared/model/nutrition';
import {
  createCommentModal,
  createPeriodModal,
  hideModal
} from '../lib/cancellation-modal-utils';
import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import {DEFAULT_DATE} from '../../../7_shared/consts/default_date';
import {CommentFormData} from '../../../5_features/modal-nutrition-comment';
import {magicModal} from 'react-native-magic-modal';
import {CancelNutritionIn} from '../../../5_features/nutrition/api/types';

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
      setNutritionInfoState({
        ...nutritionInfoState,
        cancellationPeriods: cancelData
      });
    }
  }, [isCanceledSuccess]);

  useEffect(() => {
    if (isResumedSuccess) {
      setNutritionInfoState({
        ...nutritionInfoState,
        cancellationPeriods: resumeData
      });
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
      setNutritionInfoState(nutritionInfo as PupilNutritionInfo);
    }
  };

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

  const showCancellationModal = () => {
    magicModal.show(() => createPeriodModal(selectedDate, {
      onConfirm: showCommentModal,
      onClose: () => {
        hideModal();
      }
    }));
  };

  const showCommentModal = async (startingDate: Date, endingDate: Date) => {
    await hideModal();
    magicModal.show(() => createCommentModal({
      onSendClick: async (commentData: CommentFormData) => {
        await sendCancellation({
          startsAt: dateToString(startingDate),
          endsAt: dateToString(endingDate),
          reason: commentData.reason
        });
        await hideModal();
      }
    }));
  };

  const sendCancellation = async (body: CancelNutritionIn['body']) => {
    await cancelNutrition({
      pupilId: props.pupilId,
      body: body
    });
  };

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
