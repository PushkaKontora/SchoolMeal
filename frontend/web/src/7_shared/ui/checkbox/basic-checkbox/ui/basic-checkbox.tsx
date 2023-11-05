import { useState } from 'react';

import '../consts/style.scss';
import { BasicCheckboxProps } from '../model/props';

export default function BasicCheckbox(props: BasicCheckboxProps) {
  const { isDisable, isCheck } = props;
  const [isChecked, setIsChecked] = useState(isCheck);

  return (
    <label>
      <input
        type='checkbox'
        onChange={() => {
          setIsChecked(!isChecked);
        }}
      />
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
