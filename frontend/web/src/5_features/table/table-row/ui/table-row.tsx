import { useEffect } from 'react';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableRowProps } from '../model/props';
import { ValueBadge } from '../../../../7_shared/ui/special/value-badge';

export default function TableRow(props: TableRowProps) {
  const { name, balance, total } = props;

  let isBalancePositive = true;

  useEffect(() => {
    if (balance[0] === '-') {
      isBalancePositive = !isBalancePositive;
    }
  }, [balance]);

  return (
    <tr>
      <td scope='col'  className='checkChild'>
        <BasicCheckbox />
        <ValueBadge
          value={`${balance} ₽`}
          textColor={isBalancePositive ? '#58BCBB' : '#EC662A'}
          width='60px'
        />
        <div className='nameChild'>{name}</div>
      </td>
      <td scope='row'>
        <BasicCheckbox />
      </td>
      <td scope='row'>
        <BasicCheckbox />
      </td>
      <td scope='row'>
        <BasicCheckbox />
      </td>
      <td scope='row'>
        <ValueBadge
          value={`${total ? total : 0} ₽`}
          textColor={'#58BCBB'}
          width='52px'
          margin='auto 0 auto auto'
        />
      </td>
    </tr>
  );
}
