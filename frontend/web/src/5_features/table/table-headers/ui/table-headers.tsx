import { useAppDispatch } from '../../../../../store/hooks';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableHeadersProps } from '../model/props';

export default function TableHeaders(props: TableHeadersProps) {
  const { price } = props;
  const dispatch = useAppDispatch();

  return (
    <tr>
      <td scope='col' className='col_name'>
        {/* <BasicCheckbox isDisable={false} /> */}
        <span className='spanName'>ФИО</span>
      </td>
      <td scope='col'>
        <div className='nameCol'>Завтрак</div>
        {price && <div className='price'>{price[0]} ₽</div>}
        <BasicCheckbox isDisable={false} isCheck={false} type='b' isHeader={true}/>
      </td>
      <td scope='col'>
        <div className='nameCol'>Обед</div>
        {price && <div className='price'>{price[1]} ₽</div>}
        <BasicCheckbox isDisable={false} isCheck={false} type='l' isHeader={true}/>
      </td>
      <td scope='col'>
        <div className='nameCol'>Полдник</div>
        {price && <div className='price'>{price[2]} ₽</div>}
        <BasicCheckbox isDisable={false} isCheck={false} type='s' isHeader={true}/>
      </td>
      <td scope='col'>
        <div className='nameCol'>Итого</div>
      </td>
    </tr>
  );
}
