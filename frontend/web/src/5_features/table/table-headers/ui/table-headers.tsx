import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableHeadersProps } from '../model/props';

export default function TableHeaders(props: TableHeadersProps) {
  const { price } = props;

  return (
    <tr>
      <td scope='col' className='col_name'>
        <BasicCheckbox />
        <span className='spanName'>ФИО</span>
      </td>
      <td scope='col'>
        <div className='nameCol'>Завтрак</div>
        {price && <div className='price'>{price[0]} ₽</div>}
      </td>
      <td scope='col'>
        <div className='nameCol'>Обед</div>
        {price && <div className='price'>{price[1]} ₽</div>}
      </td>
      <td scope='col'>
        <div className='nameCol'>Ужин</div>
        {price && <div className='price'>{price[2]} ₽</div>}
      </td>
      <td scope='col'>
        <div className='nameCol'>Итого</div>
      </td>
    </tr>
  );
}
