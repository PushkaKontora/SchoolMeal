import {ScrollView, View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/props';
import {useEffect, useState} from 'react';
import {isEnoughMealAmountToShow, isFeeding} from '../lib/utils';
import {useChangeNutritionPlanMutation, useGetPupilNutritionQuery} from '../../../5_features/nutrition/api';
import {NutritionPlan} from '../../../7_shared/model/nutrition';

export function NutritionWidget(props: NutritionWidgetProps) {
  // === states ===
  const [showToogles, setShowToogles] = useState(true);

  const [mealData, setMealData] = useState<NutritionPlan>({
    hasBreakfast: false,
    hasDinner: false,
    hasSnacks: false
  });
  const [feeding, setFeeding] = useState(isFeeding(mealData));

  // === variables ===

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
    setShowToogles(feeding && isEnoughMealAmountToShow(mealData));
  }, [feeding, mealData]);

  // === functions ===

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
            showToogles &&
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
              pupilId={props.pupilId}/>
          }

        </View>
      </View>
    </ScrollView>
  );
}
