import {Container} from './styles.ts';
import {DefaultInputs, NutritionClassList} from '../../../5_features/nutrition-class-list-feature';
import {NutritionClassListWidgetProps} from '../model/props.ts';

export function NutritionClassListWidget(props: NutritionClassListWidgetProps) {
  return (
    <Container>
      <DefaultInputs
        selectedClassIndex={props.selectedClassIndex}
        classNames={props.classNames}
        onClassSelect={props.onClassSelect}
      />
      <NutritionClassList
        data={props.data}
        tableData={props.tableData}
        updateData={props.updateData}
      />
    </Container>
  );
}
