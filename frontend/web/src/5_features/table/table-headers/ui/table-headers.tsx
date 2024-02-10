import Checkbox from '../../../../7_shared/ui/v2/interactive/check-box/ui/checkbox.tsx';
import '../consts/style.scss';
import { TableHeadersProps } from '../model/props';

export default function TableHeaders(props: TableHeadersProps) {
  const { breakfastPrice, lunchPrice, snackPrice } = props;

  return (
    <tr className='tableHeader'>
      <td scope='col' className='col_name'>
        {/* <Checkbox isDisable={false} /> */}
        <span className='spanName'>ФИО</span>
      </td>
      <td scope='col' className='tableHeaderCell tableHeaderCell__breakfast'>
        <div className='nameCol'>Завтрак</div>
        {breakfastPrice && <div className='price'>{breakfastPrice} ₽</div>}
        <Checkbox
          isDisable={false}
          isCheck={false}
          type='b'
          isHeader={true}
        />
      </td>
      <td scope='col' className='tableHeaderCell'>
        <div className='nameCol'>Обед</div>
        {lunchPrice && <div className='price'>{lunchPrice} ₽</div>}
        <Checkbox
          isDisable={false}
          isCheck={false}
          type='l'
          isHeader={true}
        />
      </td>
      <td scope='col' className='tableHeaderCell snack'>
        <div className='nameCol'>Полдник</div>
        {snackPrice && <div className='price'>{snackPrice} ₽</div>}
        <Checkbox
          isDisable={false}
          isCheck={false}
          type='s'
          isHeader={true}
        />
      </td>
    </tr>
  );
}
