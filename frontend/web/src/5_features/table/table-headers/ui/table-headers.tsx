import { useAppDispatch } from '../../../../../store/hooks';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableHeadersProps } from '../model/props';

export default function TableHeaders(props: TableHeadersProps) {
  const { breakfastPrice, lunchPrice, snackPrice } = props;
  const dispatch = useAppDispatch();

  return (
    <tr>
      <td scope='col' className='col_name'>
        {/* <BasicCheckbox isDisable={false} /> */}
        <span className='spanName'>ФИО</span>
      </td>
      <td scope='col'>
        <div className='nameCol'>Завтрак</div>
        {breakfastPrice && <div className='price'>{breakfastPrice} ₽</div>}
        <BasicCheckbox
          isDisable={false}
          isCheck={false}
          type='b'
          isHeader={true}
        />
      </td>
      <td scope='col'>
        <div className='nameCol'>Обед</div>
        {lunchPrice && <div className='price'>{lunchPrice} ₽</div>}
        <BasicCheckbox
          isDisable={false}
          isCheck={false}
          type='l'
          isHeader={true}
        />
      </td>
      <td scope='col'>
        <div className='nameCol'>Полдник</div>
        {snackPrice && <div className='price'>{snackPrice} ₽</div>}
        <BasicCheckbox
          isDisable={false}
          isCheck={false}
          type='s'
          isHeader={true}
        />
      </td>
      <td scope='col'>
       
      </td>
    </tr>
  );
}
