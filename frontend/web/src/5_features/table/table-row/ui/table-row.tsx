import { useEffect, useState } from 'react';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableRowProps } from '../model/props';
import { ValueBadge } from '../../../../7_shared/ui/special/value-badge';

export default function TableRow(props: TableRowProps) {
  const { name, balance, total, breakfast, lunch, snack } = props;

  const [arrayCheckbox, setarrayCheckbox] = useState([false, false, false]);

  return (
    <tr>
      <td scope='col' className='checkChild'>
        <BasicCheckbox isDisable={breakfast && lunch && snack} />
        <ValueBadge
          value={`${balance} ₽`}
          textColor={balance[0] !== '-' ? '#58BCBB' : '#EC662A'}
          width='60px'
        />
        <div className='nameChild'>{name}</div>
      </td>
      <td scope='row'>
        <BasicCheckbox isDisable={breakfast} />
      </td>
      <td scope='row'>
        <BasicCheckbox isDisable={lunch} />
      </td>
      <td scope='row'>
        <BasicCheckbox isDisable={snack} />
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
