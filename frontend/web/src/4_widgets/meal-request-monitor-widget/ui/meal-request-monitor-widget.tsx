import {Container} from './styles.ts';
import {MealRequestMonitor} from '../../../5_features/meal-request-monitor-feature';
import {MealRequestMonitorWidgetProps} from '../model/props.ts';
import {transformData} from '../lib/transform-data.ts';
import {DefaultInputs} from '../../../5_features/meal-request-monitor-feature/ui/default-inputs';

export function MealRequestMonitorWidget(props: MealRequestMonitorWidgetProps) {
  return (
    <Container>
      <DefaultInputs
        date={props.date}
        selectedClassIndex={props.selectedClassIndex}
        classNames={props.classNames}
        onClassSelect={props.onClassSelect}
        onDateSelect={props.onDateSelect}/>
      <MealRequestMonitor
        data={transformData(props.rawData)}/>
    </Container>
  );
}
