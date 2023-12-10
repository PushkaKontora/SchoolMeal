import '../consts/style.scss';
import leftArrow from '../assets/images/leftArrow.jpg';
import rightArrow from '../assets/images/rightArrow.jpg';
import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../../../../../store/hooks';
import { getDayName } from '../../../special/dates/lib/dates-utils';
import { getMonthShortName } from '../../../special/dates/lib/month-utils';
import { selectionNewDate } from '../../../special/dates/model/date-teacher-table-slice';

export default function MonthSelection() {
  const currentDate = useAppSelector(
    (state) => state.dateTeacherTable.currentDate
  );
  const dispatch = useAppDispatch();

  const [date, setDate] = useState(new Date(currentDate));

  useEffect(() => {
    setDate(new Date(currentDate));
  }, [currentDate]);

  const onDatePickerLeftPress = () => {
    const prevDate = new Date(date.setDate(date.getDate() - 1));
    dispatch(selectionNewDate({ currentDate: prevDate.toString() }));
  };

  const onDatePickerRightPress = () => {
    const nextDay = new Date(date.setDate(date.getDate() + 1));
    dispatch(selectionNewDate({ currentDate: nextDay.toString() }));
  };

  return (
    <div className='date'>
      <img
        className='arrow'
        src={leftArrow}
        alt='this is top image'
        onClick={onDatePickerLeftPress}
      />
      <div className='text'>
        {getDayName(date)} {date.getDate()}.{getMonthShortName(date)}
      </div>
      <img
        className='arrow'
        src={rightArrow}
        alt='this is top image'
        onClick={onDatePickerRightPress}
      />
    </div>
  );
}
