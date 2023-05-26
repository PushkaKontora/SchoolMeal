import {View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/props';
import {useEffect, useState} from 'react';
import {useChangeMealPlanMutation, useGetChildByIdQuery} from '../../../6_entities/child/api/config';
import {isFeeding} from '../lib/check-utils';
import {ChildMealData} from '../../../6_entities/child/types/child-meal-data';

export function NutritionWidget(props: NutritionWidgetProps) {
  // === states ===
  const [mealData, setMealData] = useState<ChildMealData>({
    breakfast: false,
    lunch: false,
    dinner: false
  });
  const [feeding, setFeeding] = useState(isFeeding(mealData));

  // === variables ===

  const [changeMeal, {isSuccess: isChangingMealSuccess}] = useChangeMealPlanMutation();

  const {data: child, isSuccess: childSuccess, refetch: refetchChild} = useGetChildByIdQuery(props.childId);

  // === useEffects ===

  useEffect(() => {
    refetchChild();
  }, []);

  useEffect(() => {
    init();
  }, [child]);

  useEffect(() => {
    setFeeding(isFeeding(mealData));
  }, [mealData]);

  // === functions ===

  const init = () => {
    if (childSuccess) {
      const newMealData = {
        breakfast: child.breakfast,
        lunch: child.lunch,
        dinner: child.dinner
      };

      setMealData(newMealData);
    }
  };

  const onCheckChange = async (changedProperties: Partial<ChildMealData>) => {
    if (child) {
      const newMealData = {
        ...mealData,
        ...changedProperties
      };

      await changeMeal({
        childId: child.id,
        ...newMealData
      });

      setMealData(newMealData);
    }
  };

  const onHeaderCheckChange = async (turnedOn: boolean) => {
    await onCheckChange({
      breakfast: turnedOn,
      lunch: turnedOn,
      dinner: turnedOn
    });
  };

  // === render ===

  return (
    <View
      style={styles.background}>
      <View
        style={styles.card}>

        <NutritionHeaderFeature
          child={child}
          onToggle={(turnedOn: boolean) => onHeaderCheckChange(turnedOn)}
          defaultToggleState={feeding}/>

        <NutritionCertFeature
          child={child}/>

        <NutritionTogglesFeature
          onToggleBreakfast={(turnedOn: boolean) => {onCheckChange({breakfast: turnedOn});}}
          onToggleLunch={(turnedOn: boolean) => {onCheckChange({lunch: turnedOn});}}
          onToggleAfternoonSnack={(turnedOn: boolean) => {onCheckChange({dinner: turnedOn});}}
          breakfastState={mealData?.breakfast}
          lunchState={mealData?.lunch}
          afternoonSnackState={mealData?.dinner}/>

        <NutritionPanel
          child={child}
          refetchChild={refetchChild}/>

      </View>
    </View>
  );
}
