import { useEffect, useState } from 'react';

import '../consts/style.scss';
import { BasicCheckboxProps } from '../model/props';
import { useAppSelector, useAppDispatch } from '../../../../../../store/hooks';
import { changeStateCheckbox } from '../../../../../5_features/table/model/checkbox-slice.ts/checkbox-slice';

export default function BasicCheckbox(props: BasicCheckboxProps) {
  const { isDisable, isCheck, type, isHeader, onChange } = props;
  const [isChecked, setIsChecked] = useState(isCheck);
  const valueHeader = useAppSelector((state) => state.checkbox.isAction);
  const typeChangeHeaders = useAppSelector((state) => state.checkbox.type);
  const valueChangeHeaders = useAppSelector(
    (state) => state.checkbox.lastValue
  );
  const dispatch = useAppDispatch();

  useEffect(() => {
    setIsChecked(isCheck);
  }, [isCheck]);

  useEffect(() => {
    if (isHeader == false) {
      if (type === typeChangeHeaders) {
        setIsChecked(!valueChangeHeaders);
        
        if (onChange) {
          onChange(!isChecked);
        }
      }
    }
  }, [valueHeader]);

  const onCheck = () => {
    setIsChecked(!isChecked);

    if (isHeader == true) {
      dispatch(changeStateCheckbox({ type: type, value: isChecked }));
    }

    if (onChange) {
      onChange(!isChecked);
    }
  };

  return (
    <label>
      <input type='checkbox' onChange={onCheck} />
      <svg
        className={`checkbox ${
          isDisable ? 'checkbox--disabled' : isChecked ? 'checkbox--active' : ''
        }`}
        // This element is purely decorative so
        // we hide it for screen readers
        aria-hidden='true'
        width='10'
        height='8'
        viewBox='0 0 10 8'
        fill='none'
      >
        <path
          d='M8.73327 1.43396L3.59994 6.56729L1.2666 4.23396'
          strokeWidth='1.2'
          stroke={isChecked ? '#fff' : 'none'} // only show the checkmark when `isCheck` is `true`
        />
      </svg>
    </label>
  );
}
