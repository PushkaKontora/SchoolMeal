import {Sidebar, SidebarWithContent} from '../../../7_shared/ui/v2/sidebar';
import {PageStyles} from '../styles/page-styles.ts';
import {MealApplicationWidget} from '../../../4_widgets/meal-application-widget';
import {updateDataState} from '../../../7_shared/lib/react-table-wrapper';
import {MealRequestStatus} from '../../../7_shared/model/meal-request-status.ts';
import {TitleWidget} from '../../../4_widgets/title-widget';
import {
  useGetCurrentUserQuery,
  useGetMenuQuery,
  useGetPlanningMealRequestQuery,
  useGetPupilsQuery,
  useGetTeacherSchoolClassesQuery,
  usePrepareMealRequestMutation
} from '../../../7_shared/api';
import {useEffect, useState} from 'react';
import {getDefaultDate} from '../lib/get-default-date.ts';
import {skipToken} from '@reduxjs/toolkit/query';
import {dateToISOWithoutTime} from '../../../7_shared/lib/date';
import {combineTableData, createClassNames, createHeaders} from '../lib/adapters.ts';
import {MealRequestRowViewData} from '../../../6_entities/meal-request';
import {OverridenPupil} from '../../../7_shared/model/pupil.ts';

export function MealApplicationPage() {
  const [classIndex, setClassIndex] = useState<number>(0);
  const [date, setDate] = useState(new Date('2024-02-15'));

  const [tableData, setTableData]
    = useState<MealRequestRowViewData[]>([]);
  const [overridenPupils, setOverridenPupils]
    = useState<{[pupilId: OverridenPupil['id']]: OverridenPupil}>({});

  const {data: currentUser}
    = useGetCurrentUserQuery();
  const {data: classes}
    = useGetTeacherSchoolClassesQuery(currentUser?.id ?? skipToken);
  const {data: pupils, isFetching: isPupilsFetching}
    = useGetPupilsQuery(classes?.[classIndex].id ?? skipToken);
  const {data: menu}
    = useGetMenuQuery({
      school_class_number: classes?.[classIndex].initials.number || 1,
      on_date: dateToISOWithoutTime(date)
    }, { skip: !classes });
  const {data: planningRequest,
    isFetching: isPlanningReportFetching,
    refetch: refetchPlanningRequest}
    = useGetPlanningMealRequestQuery({
      class_id: classes?.[classIndex].id || '',
      on_date: dateToISOWithoutTime(date)
    }, { skip: !classes });
  
  const [prepareReport]
    = usePrepareMealRequestMutation();

  useEffect(() => {
    if (!isPupilsFetching && !isPlanningReportFetching) {
      setTableData(combineTableData(date, planningRequest, pupils));
    }
  }, [date, planningRequest, pupils, isPupilsFetching, isPlanningReportFetching]);

  return (
    <PageStyles>
      <SidebarWithContent
        sidebar={<Sidebar/>}
        contentStyles={{
          padding: '48px 40px 0 40px'
        }}>
        <TitleWidget
          title={'Подать заявку'}/>
        <MealApplicationWidget
          selected={classIndex}
          classNames={createClassNames(classes)}
          onClassSelect={(index) => setClassIndex(index)}
          onDateSelect={() => {return;}}
          data={tableData}
          updateData={(rowIndex, columnId, value) => {
            const pupilView = tableData[rowIndex];
            const pupil = pupils?.[rowIndex];
            setOverridenPupils(prev => {
              if (pupil) {
                prev[pupil.id] = {
                  id: pupil.id,
                  breakfast: pupilView.breakfast,
                  dinner: pupilView.dinner,
                  snacks: pupilView.snacks,
                  [columnId]: value
                };
              }

              return prev;
            });

            updateDataState(setTableData, rowIndex, columnId, value);
          }}
          headerViewData={createHeaders(menu)}
          status={planningRequest?.status || MealRequestStatus.NotApplied}
          buttonTitles={{
            [MealRequestStatus.Applied]: 'Редактировать',
            [MealRequestStatus.Edit]: 'Сохранить изменения',
            [MealRequestStatus.NotApplied]: 'Отправить заявку'
          }}
          onSend={() => {
            switch (planningRequest?.status) {
            case MealRequestStatus.NotApplied:
            case MealRequestStatus.Edit:
              if (classes) {
                prepareReport({
                  class_id: classes[classIndex].id,
                  on_date: dateToISOWithoutTime(date),
                  overriden_pupils: Object.values(overridenPupils)
                });
              }
              break;
            case MealRequestStatus.Applied:

              break;
            }
          }}/>
      </SidebarWithContent>
    </PageStyles>
  );
}
