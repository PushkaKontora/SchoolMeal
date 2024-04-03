
import {DefaultInputProps} from '../../../5_features/meal-request-monitor-feature/ui/default-inputs';
import {PortionsReport} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/portions.ts';

export type MealRequestMonitorWidgetProps = {
  rawData?: PortionsReport
} & DefaultInputProps;
