import {PageStyles} from '../styles/page-styles.ts';
import {MealApplicationWidget} from '../../../4_widgets/meal-application-widget';
import {updateDataState} from '../../../7_shared/lib/react-table-wrapper';
import {TitleWidget} from '../../../4_widgets/title-widget';

import {useEffect, useState} from 'react';
import {MealRequestRowViewData, schoolClassToTableViewData} from '../../../6_entities/meal-request';
import {
  booleansToMealtimeArray,
  isListEditable,
  MealApplicationFormStatus
} from '../../../5_features/meal-application-feature';
import {useAppSelector} from '../../../../store/hooks.ts';
import {Api} from '../../../7_shared/api';
import {combineTableData} from '../lib/table-data.ts';
import {toMealApplicationFormStatus} from '../lib/meal-application-form-status.ts';
import {createClassNames} from '../../../6_entities/school-class';
import {Pupil} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/pupil.ts';

export function MealApplicationPage() {
  const [classIndex, setClassIndex] = useState<number>(0);
  const [date, setDate] = useState(new Date());

  const [tableData, setTableData]
    = useState<MealRequestRowViewData[]>([]);
  const [overriddenPupils, setOverriddenPupils]
    = useState<{[pupilId: Pupil['id']]: Pick<MealRequestRowViewData, 'breakfast' | 'dinner' | 'snacks'>}>({});

  const [applicationFormStatus, setApplicationFormStatus]
    = useState<MealApplicationFormStatus | undefined>(undefined);
  const [prevTableData, setPrevTableData]
    = useState<MealRequestRowViewData[]>([]);

  const currentUserId
    = useAppSelector(state => state['auth'].jwtPayload?.user_id);

  const {data: classes} 
    = Api.useGetSchoolClassesQuery({
      teacherId: currentUserId!
    }, {skip: currentUserId === undefined});
  const {data: prefilledRequest, isSuccess: isPrefilledSuccess}
    = Api.usePrefillNutritionRequestQuery({
      classId: classes?.[classIndex].id || '',
      date: date
    }, {skip: !classes});
  const [sendNutritionRequest]
    = Api.useSendNutritionRequestMutation();

  useEffect(() => {
    if (prefilledRequest && isPrefilledSuccess) {
      setTableData(combineTableData(prefilledRequest));
      setApplicationFormStatus(toMealApplicationFormStatus(prefilledRequest.status));
    }
  }, [prefilledRequest, isPrefilledSuccess]);

  return (
    <PageStyles>
      <TitleWidget
        title={'Подать заявку'}/>
      <MealApplicationWidget
        selectedClassIndex={classIndex}
        classNames={createClassNames(classes)}
        onClassSelect={(index) => setClassIndex(index)}
        date={date}
        onDateSelect={(date) => setDate(date)}
        data={tableData}
        tableData={{
          editable: isListEditable(applicationFormStatus),
          ...schoolClassToTableViewData(classes?.[classIndex])
        }}
        updateData={(rowIndex, columnId, value) => {
          const pupilView = tableData[rowIndex];
          const pupil = prefilledRequest?.pupils?.[rowIndex];
          setOverriddenPupils(prev => {
            if (pupil) {
              prev[pupil.id] = {
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
        status={applicationFormStatus || MealApplicationFormStatus.NotApplied}
        buttonTitles={{
          [MealApplicationFormStatus.Applied]: 'Редактировать',
          [MealApplicationFormStatus.Edit]: 'Сохранить изменения',
          [MealApplicationFormStatus.NotApplied]: 'Отправить заявку'
        }}
        onCancel={() => {
          setApplicationFormStatus(toMealApplicationFormStatus(prefilledRequest?.status));
          setTableData(prevTableData);
          setOverriddenPupils({});
        }}
        onSend={() => {
          switch (applicationFormStatus) {
          case MealApplicationFormStatus.NotApplied:
          case MealApplicationFormStatus.Edit:
            if (classes) {
              sendNutritionRequest({
                classId: classes[classIndex].id,
                date: date,
                overrides: Object.keys(overriddenPupils).map(pupilId => ({
                  id: pupilId,
                  mealtimes: booleansToMealtimeArray(overriddenPupils[pupilId])
                }))
              });
            }
            break;
          case MealApplicationFormStatus.Applied:
            setPrevTableData(tableData);
            setApplicationFormStatus(MealApplicationFormStatus.Edit);
            break;
          }
        }}/>
    </PageStyles>
  );
}
