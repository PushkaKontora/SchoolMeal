import {ScrollView, View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';
import {NutritionWidgetProps} from '../types/props';
import {useEffect, useState} from 'react';
import {useChangeMealPlanMutation, useGetChildByIdQuery} from '../../../6_entities/child/api/config';
import {isEnoughMealAmountToShow, isFeeding} from '../lib/utils';
import {ChildMealData} from '../../../6_entities/child/types/child-meal-data';
import {getMealAmount} from '../../../6_entities/school-class/lib/class-utils';

export function NutritionWidget(props: NutritionWidgetProps) {
  // === states ===
  const [mealAmount, setMealAmount] = useState(3);

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
      setMealAmount(getMealAmount(child.schoolClass));
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
    <ScrollView>
      <View
        style={styles.background}>
        <View
          style={styles.card}>

          <NutritionHeaderFeature
            child={child}
            onToggle={(toggledRight: boolean) => onHeaderCheckChange(!toggledRight)}
            defaultToggleState={!feeding}/>

          <NutritionCertFeature
            child={child}/>

          {
            feeding &&
            isEnoughMealAmountToShow(mealAmount) &&
            <NutritionTogglesFeature
              onToggleBreakfast={(turnedOn: boolean) => {
                onCheckChange({breakfast: turnedOn});
              }}
              onToggleLunch={(turnedOn: boolean) => {
                onCheckChange({lunch: turnedOn});
              }}
              onToggleAfternoonSnack={(turnedOn: boolean) => {
                onCheckChange({dinner: turnedOn});
              }}
              breakfastState={mealData?.breakfast}
              lunchState={mealData?.lunch}
              afternoonSnackState={mealData?.dinner}
              hasBreakfast={child?.schoolClass.hasBreakfast || false}
              hasLunch={child?.schoolClass.hasLunch || false}
              hasAfternoonSnack={child?.schoolClass.hasDinner || false}/>
          }   

          {
            feeding &&
            <NutritionPanel
              child={child}
              refetchChild={refetchChild}/>
          }

        </View>
      </View>
    </ScrollView>
  );
}
