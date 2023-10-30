import {TableContainer, Tabs, Title} from './styles';
import {MealClassTable} from '../../../5_features/meals/meal-class-table';
import {MealInfoTable} from '../../../5_features/meals/meal-info-table';
import {Content} from '../../../7_shared/ui/markup/content';
import {useGetMealRequestsQuery} from '../../../6_entities/meals/api/api';
import {GetMealRequestsParams} from '../../../6_entities/meals/api/types';
import {useEffect, useState} from 'react';
import {MealRowData} from '../types/meal-row-data';
import {sortMealsOfDate} from '../lib/utils';
import {BREAKFAST_TITLE, DINNER_TITLE, LUNCH_TITLE} from '../consts/titles';
import HeaderTeacherWidget from '../../header-teacher/ui/header-teacher';
import {CLASS_TITLES, TITLE} from '../config/config';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary';

export function MealApplicationWidget() {
  const params: GetMealRequestsParams = {
    date: '2023-06-14'
  };
  const {data: mealRequests} = useGetMealRequestsQuery(params);

  const [mealRowData, setMealRowData] = useState<MealRowData | null>(null);
  //const [totalMealRowData, setTotalMealRowData] = useState<MealRowValue | null>(null);

  useEffect(() => {
    if (mealRequests) {
      setMealRowData(sortMealsOfDate(mealRequests));
    }
  }, [mealRequests]);

  return (
    <div>
      <Content>
        <HeaderTeacherWidget/>

        <Title>
          {TITLE}
        </Title>

        <Tabs>
          <ButtonSecondary
            title={CLASS_TITLES.elementary}
            onPress={() => {return;}}/>
          <ButtonSecondary
            title={CLASS_TITLES.high}
            disabled
            onPress={() => {return;}}/>
        </Tabs>

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
                  .map(item => item.lunch)) || []
            }/>

          <MealInfoTable
            width={'25%'}
            title={DINNER_TITLE}
            showMissingValues={true}
            data={
              (mealRowData &&
                Object.values(mealRowData)
                  .map(item => item.dinner)) || []
            }/>
        </TableContainer>
      </Content>
    </div>
  );
}
