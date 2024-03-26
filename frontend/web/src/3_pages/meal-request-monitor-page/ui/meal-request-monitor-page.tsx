import {
  MealRequestMonitorWidget
} from '../../../4_widgets/meal-request-monitor-widget/ui/meal-request-monitor-widget.tsx';
import {useGetReportQuery} from '../../../7_shared/api/deprecated/api.ts';
import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import {PageStyles} from './styles.ts';
import {useState} from 'react';
import {CLASS_NAMES, ClassTypesByIndex} from '../const/classes.ts';
import {TitleWidget} from '../../../4_widgets/title-widget';

export function MealRequestMonitorPage() {
  const [date, setDate] = useState(new Date());
  const [classIndex, setClassIndex] = useState<number>(0);

  const {data: mealRequest} = useGetReportQuery({
    class_type: ClassTypesByIndex[classIndex],
    on_date: dateToISOWithoutTime(date)
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
