import {NutritionClassListWidget} from '../../../4_widgets/nutrition-class-list-widget';
import {useEffect, useState} from 'react';
import {createClassNames} from '../../../6_entities/school-class';
import {toTableRowViewDataArray, toTableViewData} from '../lib/mappers.ts';
import {useAppSelector} from '../../../../store/hooks.ts';
import {updateDataState} from '../../../7_shared/lib/react-table-wrapper';
import {PageStyles} from './styles.ts';
import {TitleWidget} from '../../../4_widgets/title-widget';
import {Api} from '../../../7_shared/api';
import {TableRowViewData} from '../../../6_entities/meal-plan';

export function NutritionClassListPage() {
  const userId = useAppSelector(state => state['auth'].jwtPayload?.user_id);

  const [classIndex, setClassIndex] = useState(0);

  const {data: classes} = Api.useGetSchoolClassesQuery({
    teacherId: userId!
  }, {skip: !userId});
  const {data: pupils, isSuccess: isPupilsSuccess} = Api.useGetPupilsQuery({
    classId: classes?.[classIndex]?.id
  }, {skip: !classes, refetchOnMountOrArgChange: true});
  const [updateMealtimes] = Api.useUpdatePupilMealtimesMutation();

  const [tableData, setTableData]
    = useState<TableRowViewData[]>([]);

  useEffect(() => {
    if (pupils && isPupilsSuccess)
      setTableData(toTableRowViewDataArray(pupils));
  }, [isPupilsSuccess, pupils]);
  
  return (
    <PageStyles>
      <TitleWidget
        title={'Мои классы'}
        subtitle={'Здесь вы можете поставить ребенка на постоянное питание'}/>
      <NutritionClassListWidget
        data={tableData}
        tableData={toTableViewData(classes?.[classIndex].mealtimes)}
        updateData={(rowIndex, columnId, value) => {
          if (pupils) {
            updateMealtimes({
              pupilId: pupils[rowIndex].id,
              mealtimes: {
                [columnId]: value
              }
            });
          }
          updateDataState(setTableData, rowIndex, columnId, value);
        }}
        selectedClassIndex={classIndex}
        classNames={createClassNames(classes)}
        onClassSelect={setClassIndex}/>
    </PageStyles>
  );
}
