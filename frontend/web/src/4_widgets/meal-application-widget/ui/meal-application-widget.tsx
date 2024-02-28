import {Container} from './styles.ts';
import {DefaultInputs, MealApplicationForm} from '../../../5_features/meal-application-feature';
import {MealApplicationWidgetProps} from '../model/props.ts';

export function MealApplicationWidget(props: MealApplicationWidgetProps) {
  return (
    <Container>
      <DefaultInputs
        date={props.date}
        selectedClassIndex={props.selectedClassIndex}
        classNames={props.classNames}
        onClassSelect={props.onClassSelect}
        onDateSelect={props.onDateSelect}/>
      <MealApplicationForm
        data={props.data}
        updateData={props.updateData}
        headerViewData={props.headerViewData}
        status={props.status}
        buttonTitles={props.buttonTitles}
        onSend={props.onSend}/>
    </Container>
  );
}
