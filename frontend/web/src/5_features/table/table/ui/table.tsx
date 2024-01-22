import '../consts/style.scss';
import { CHILDRENS_NAME } from '../../../../3_pages/teacher-main-page/consts/moks.ts';
import TableHeaders from '../../table-headers/ui/table-headers.tsx';
import TableRow from '../../table-row/ui/table-row.tsx';
import { useAppSelector, useAppDispatch } from '../../../../../store/hooks.ts';
import { useEffect } from 'react';
import { usePupilsQuery } from '../../../../6_entities/nutrition/api/api.ts';
import { PupilItemApi } from '../../../../6_entities/nutrition/model/PlanReport.ts';
import {
  fillPlanReportStatus,
  fillPrepareItems,
} from '../../../tabs/class-selection/model/class-tabs-slice.ts';

export default function Table() {
  const сlassID = useAppSelector((state) => state.classTabs.classID);
  const dataCh = useAppSelector((state) => state.classTabs.dataCh);

  const dispatch = useAppDispatch();

  const { data: planReport, refetch: refPupils } = usePupilsQuery({
    class_id: сlassID,
    on_date: dataCh,
  });

  useEffect(() => {
    if (сlassID && dataCh) {
      refPupils();
    }
  }, [сlassID, dataCh, refPupils]);

  useEffect(() => {
    if (planReport) {
      dispatch(fillPlanReportStatus(planReport.status));
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [planReport]);

  return (
    <div className='containerTable'>
      <table className='planReportTable'>
        <thead className='containerHead'>
          <TableHeaders
            breakfastPrice={CHILDRENS_NAME[0].breakfast.price}
            lunchPrice={CHILDRENS_NAME[0].lunch.price}
            snackPrice={CHILDRENS_NAME[0].snack.price}
          />
        </thead>
        <tbody className='containerBody'>
          {planReport &&
            planReport.pupils.map((item: PupilItemApi) => (
              <TableRow
                name={item.last_name + ' ' + item.first_name}
                //balance={item.price.toString()}
                // total={item?.total}
                key={item.id}
                breakfast={item.breakfast}
                lunch={item.dinner}
                snack={item.snacks}
                onChange={(breakfast, lunch, snack) => {
                  dispatch(
                    fillPrepareItems({
                      id: item.id,
                      breakfast: breakfast,
                      dinner: lunch,
                      snacks: snack,
                    })
                  );
                }}
              />
            ))}
        </tbody>
      </table>
    </div>
  );
}
