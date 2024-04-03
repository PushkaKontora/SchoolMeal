import {
  MealRequestMonitorWidget
} from '../../../4_widgets/meal-request-monitor-widget/ui/meal-request-monitor-widget.tsx';
import {PageStyles} from './styles.ts';
import {useState} from 'react';
import {CLASS_NAMES, ClassTypesByIndex} from '../const/classes.ts';
import {TitleWidget} from '../../../4_widgets/title-widget';
import {Api} from '../../../7_shared/api';

export function MealRequestMonitorPage() {
  const [date, setDate] = useState(new Date());
  const [classIndex, setClassIndex] = useState<number>(0);

  const {data: mealRequest} = Api.useGetPortionsQuery({
    classType: ClassTypesByIndex[classIndex],
    date: date
  });

  return (
    <PageStyles>
      <TitleWidget
        title={'Заявки на питание'}/>
      <MealRequestMonitorWidget
        rawData={mealRequest}
        date={date}
        onDateSelect={setDate}
        onClassSelect={setClassIndex}
        classNames={CLASS_NAMES}
        selectedClassIndex={classIndex}
      />
    </PageStyles>
  );
}
