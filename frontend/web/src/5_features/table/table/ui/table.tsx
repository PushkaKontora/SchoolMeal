import '../consts/style.scss';
import { CHILDRENS_NAME } from '../../../../3_pages/teacher-main-page/consts/moks.ts';
import TableHeaders from '../../table-headers/ui/table-headers.tsx';
import TableRow from '../../table-row/ui/table-row.tsx';
import { useAppSelector } from '../../../../../store/hooks.ts';
import { useEffect } from 'react';
import { usePupilsQuery } from '../../../../6_entities/nutrition/api/api.ts';
import { Pupil } from '../../../../6_entities/meals/model/pupil-view.ts';

export default function Table() {
  const initialsActiveClass = useAppSelector(
    (state) => state.classTabs.activeClass
  );
  const сlassID = useAppSelector((state) => state.classTabs.classID);
  const { data: pupils, refetch: refPupils } = usePupilsQuery(сlassID);

  useEffect(() => {
    console.log(сlassID, '2')
    if (сlassID) {
      refPupils();
    }
    console.log(pupils, сlassID, '3');
  }, [сlassID]);

  return (
    <div className='containerTable'>
      <table className='table'>
        <thead>
          <TableHeaders
            breakfastPrice={CHILDRENS_NAME[0].breakfast.price}
            lunchPrice={CHILDRENS_NAME[0].lunch.price}
            snackPrice={CHILDRENS_NAME[0].snack.price}
          />
        </thead>
        <tbody>
          {pupils && pupils.map((item: Pupil) => (
            <TableRow
              name={item.lastName + ' ' + item.firstName}
              //balance={item.price.toString()}
              // total={item?.total}
              key={item.id}
              breakfast={item.mealPlan.hasBreakfast}
              lunch={item.mealPlan.hasDinner}
              snack={item.mealPlan.hasSnacks}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
