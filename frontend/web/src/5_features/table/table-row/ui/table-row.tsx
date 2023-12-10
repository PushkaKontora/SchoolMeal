import { useEffect, useState } from 'react';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableRowProps } from '../model/props';
import { ValueBadge } from '../../../../7_shared/ui/special/value-badge';

export default function TableRow(props: TableRowProps) {
  const { name, balance, total, breakfast, lunch, snack } = props;

  const [breakfastCheckbox, setBreakfastCheckbox] = useState(breakfast.isCheck);
  const [lunchCheckbox, setLunchCheckbox] = useState(lunch.isCheck);
  const [snackCheckbox, setSnackCheckbox] = useState(snack.isCheck);


  const checkHandler = () => {};

  const onChangeBreakfastCheckbox = (state: boolean) => {
    setBreakfastCheckbox(state);
  };

  return (
    <tr>
      <td scope='col' className='checkChild'>
        {/* <BasicCheckbox
          isDisable={
            breakfast.isDisabled && lunch.isDisabled && snack.isDisabled
          }
          isCheck={
            (!breakfast.isDisabled &&
              breakfastCheckbox &&
              !lunch.isDisabled &&
              lunchCheckbox &&
              !snack.isDisabled &&
              snackCheckbox) ||
            (breakfast.isDisabled &&
              !lunch.isDisabled &&
              lunchCheckbox &&
              !snack.isDisabled &&
              snackCheckbox) ||
            (!breakfast.isDisabled &&
              breakfastCheckbox &&
              lunch.isDisabled &&
              !snack.isDisabled &&
              snackCheckbox) ||
            (!breakfast.isDisabled &&
              breakfastCheckbox &&
              !lunch.isDisabled &&
              lunchCheckbox &&
              snack.isDisabled) ||
            (breakfast.isDisabled &&
              lunch.isDisabled &&
              !snack.isDisabled &&
              snackCheckbox) ||
            (breakfast.isDisabled &&
              !lunch.isDisabled &&
              lunchCheckbox &&
              snack.isDisabled) ||
            (!breakfast.isDisabled &&
              breakfastCheckbox &&
              lunch.isDisabled &&
              snack.isDisabled)
          }
        /> */}
        <ValueBadge
          value={`${balance} ₽`}
          textColor={balance[0] !== '-' ? '#58BCBB' : '#EC662A'}
          width='60px'
        />
        <div className='nameChild'>{name}</div>
      </td>
      <td scope='row'>
        <BasicCheckbox
          isDisable={breakfast.isDisabled}
          isCheck={breakfastCheckbox}
          onChange={onChangeBreakfastCheckbox}
          type='b' isHeader={false}
        />
      </td>
      <td scope='row'>
        <BasicCheckbox isDisable={lunch.isDisabled} isCheck={lunch.isCheck} type='l' isHeader={false}/>
      </td>
      <td scope='row'>
        <BasicCheckbox isDisable={snack.isDisabled} isCheck={snack.isCheck} type='s' isHeader={false}/>
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
