import { useState, useEffect } from 'react';
import BasicCheckbox from '../../../../7_shared/ui/checkbox/basic-checkbox/ui/basic-checkbox';
import '../consts/style.scss';
import { TableRowProps } from '../model/props';

export default function TableRow(props: TableRowProps) {
  const { name, breakfast, lunch, snack, onChange } = props;

  const [breakfastCheckbox, setBreakfastCheckbox] = useState(breakfast);
  const [lunchCheckbox, setLunchCheckbox] = useState(lunch);
  const [snackCheckbox, setSnackCheckbox] = useState(snack);

  useEffect(() => {
    onChange(breakfastCheckbox, lunchCheckbox, snackCheckbox);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [breakfastCheckbox, lunchCheckbox, snackCheckbox]);

  // const [countTotalSum, setCountTotalSum] = useState(total);

  // useEffect(() => {
  //   let sum = 0;
  //   if (!breakfast.isDisabled && breakfastCheckbox) {
  //     sum += breakfast.price;
  //   }
  //   if (!lunch.isDisabled && lunchCheckbox) {
  //     sum += lunch.price;
  //   }
  //   if (!snack.isDisabled && snackCheckbox) {
  //     sum += snack.price;
  //   }
  //   setCountTotalSum(sum);
  // }, [breakfastCheckbox, lunchCheckbox, snackCheckbox]);

  const onChangeBreakfastCheckbox = (state: boolean) => {
    setBreakfastCheckbox(state);
  };

  const onChangeLunchCheckbox = (state: boolean) => {
    setLunchCheckbox(state);
  };

  const onChangeSnackCheckbox = (state: boolean) => {
    setSnackCheckbox(state);
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
        {/* <ValueBadge
          value={`${balance} ₽`}
          textColor={balance[0] !== '-' ? '#58BCBB' : '#EC662A'}
          width='60px'
        /> */}
        <div className='nameChild'>{name}</div>
      </td>
      <td scope='row'>
        <BasicCheckbox
          isDisable={false}
          isCheck={breakfast}
          onChange={onChangeBreakfastCheckbox}
          type='b'
          isHeader={false}
        />
      </td>
      <td scope='row'>
        <BasicCheckbox
          isDisable={false}
          isCheck={lunch}
          onChange={onChangeLunchCheckbox}
          type='l'
          isHeader={false}
        />
      </td>
      <td scope='row'>
        <BasicCheckbox
          isDisable={false}
          isCheck={snack}
          onChange={onChangeSnackCheckbox}
          type='s'
          isHeader={false}
        />
      </td>
      {/* <td scope='row'>
        <ValueBadge
          value={`${countTotalSum ? countTotalSum : 0} ₽`}
          textColor={'#58BCBB'}
          width='52px'
          margin='auto 0 auto auto'
        />
      </td> */}
    </tr>
  );
}
