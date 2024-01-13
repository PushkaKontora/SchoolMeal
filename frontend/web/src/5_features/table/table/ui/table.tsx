import '../consts/style.scss';
import { CHILDRENS_NAME } from '../../../../3_pages/teacher-main-page/consts/moks.ts';
import TableHeaders from '../../table-headers/ui/table-headers.tsx';
import TableRow from '../../table-row/ui/table-row.tsx';

export default function Table() {
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
          {CHILDRENS_NAME.map((item) => (
            <TableRow
              name={item.name}
              balance={item.price.toString()}
              total={item?.total}
              key={item.id}
              breakfast={item.breakfast}
              lunch={item.lunch}
              snack={item.snack}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
