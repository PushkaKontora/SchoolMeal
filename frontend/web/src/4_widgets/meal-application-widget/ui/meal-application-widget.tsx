import {TableContainer, Title} from './styles';
import {MealClassTable} from '../../../5_features/meals/meal-class-table';
import {MealInfoTable} from '../../../5_features/meals/meal-info-table';
import {Content} from '../../../7_shared/ui/markup/content';
import {useEffect, useState} from 'react';
import {MealRowData} from '../types/meal-row-data';
import {transformRequestReport} from '../lib/utils';
import {BREAKFAST_TITLE, DINNER_TITLE, LUNCH_TITLE} from '../consts/titles';
import HeaderTeacherWidget from '../../header-teacher/ui/header-teacher';
import {TITLE} from '../config/config';
import {useGetReportQuery} from '../../../6_entities/requests/api/api.ts';
import {dateToISOString} from '../lib/date-utils.ts';
import {RequestReportIn} from '../../../6_entities/requests/api/types.ts';
import {ClassSelector} from '../../../7_shared/ui/special/class-selector';

export function MealApplicationWidget() {
  const [date] = useState(dateToISOString(new Date()));
  const [classType, setClassType]
    = useState<RequestReportIn['classType']>('primary');
  const {data: mealRequests, refetch: refetchReport} = useGetReportQuery({
    classType: classType,
    date: date
  });

  const [mealRowData, setMealRowData] = useState<MealRowData | null>(null);

  useEffect(() => {
    refetchReport();
  }, [date, classType, refetchReport]);

  useEffect(() => {
    if (mealRequests) {
      setMealRowData(transformRequestReport(mealRequests));
    }
  }, [mealRequests]);

  return (
    <div>
      <Content>
        <HeaderTeacherWidget/>

        <Title>
          {TITLE}
        </Title>

        <ClassSelector
          config={[
            {
              name: '1-4 класс',
              onClick: () => {
                setClassType('primary');
              }
            },
            {
              name: '5-11 класс',
              onClick: () => {
                setClassType('high');
              }
            }
          ]}/>

        <TableContainer>
          <MealClassTable
            width={'25%'}
            classNames={(mealRowData && Object.keys(mealRowData)) || []}/>

          <MealInfoTable
            width={'25%'}
            title={BREAKFAST_TITLE}
            showMissingValues={true}
            data={
              (mealRowData &&
                Object.values(mealRowData)
                  .map(item => item.breakfast)) || []
            }/>

          <MealInfoTable
            width={'25%'}
            title={LUNCH_TITLE}
            showMissingValues={true}
            data={
              (mealRowData &&
                Object.values(mealRowData)
                  .map(item => item.dinner)) || []
            }/>

          <MealInfoTable
            width={'25%'}
            title={DINNER_TITLE}
            showMissingValues={true}
            data={
              (mealRowData &&
                Object.values(mealRowData)
                  .map(item => item.snacks)) || []
            }/>
        </TableContainer>
      </Content>
    </div>
  );
}
