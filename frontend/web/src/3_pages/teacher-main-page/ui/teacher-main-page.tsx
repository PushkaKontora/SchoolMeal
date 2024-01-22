/* eslint-disable react-hooks/exhaustive-deps */
import HeaderTeacherWidget from '../../../4_widgets/header-teacher/ui/header-teacher.tsx';
import {
  infoMessageTime,
  BUTTON_TEXT_SEND_ISSUE,
  BUTTON_TEXT_SAVED_CHANGED,
} from '../consts/consts.ts';
import { useEffect, useState } from 'react';
import Popup from 'reactjs-popup';
import ClassSelection from '../../../5_features/tabs/class-selection/ui/class-selection.tsx';
import MonthSelection from '../../../7_shared/ui/selection/month/ui/class-selection.tsx';
import Table from '../../../5_features/table/table/ui/table.tsx';
import {
  useSchoolClassesQuery,
  useRequestPrepareMutation,
} from '../../../6_entities/nutrition/api/api.ts';
import { useAppDispatch, useAppSelector } from '../../../../store/hooks.ts';
import {
  fillAvailableClasses,
  allTeacherClasses,
} from '../../../5_features/tabs/class-selection/model/class-tabs-slice.ts';
import { SchoolClasses } from '../../../6_entities/nutrition/model/schoolClasses.ts';
import { useCurrentUserQuery } from '../../../6_entities/user/api/api.ts';
import '../consts/style.scss';

export function TeacherMainPage() {
  const prepareItems = useAppSelector((state) => state.classTabs.prepareItems);
  const сlassID = useAppSelector((state) => state.classTabs.classID);
  const dataCh = useAppSelector((state) => state.classTabs.dataCh);
  const planReportStatus = useAppSelector(
    (state) => state.classTabs.planReportStatus
  );
  const [open, setOpen] = useState(false);
  const [prepareItemsArray, setPrepareItemsArray] = useState([]);
  const dispatch = useAppDispatch();

  const { data: currentUser } = useCurrentUserQuery();
  const { data: teacherClasses, refetch: refTeacherClasses } =
    useSchoolClassesQuery(currentUser.id);

  const [prepare, { isSuccess: preparedSuccess }] = useRequestPrepareMutation();

  useEffect(() => {
    setPrepareItemsArray(Object.values(prepareItems));
  }, [prepareItems]);

  useEffect(() => {
    if (currentUser) {
      refTeacherClasses();
    }
  }, [currentUser]);

  useEffect(() => {
    if (teacherClasses) {
      makeInitialClassList(teacherClasses);
      dispatch(allTeacherClasses({ allClassList: teacherClasses }));
    }
  }, [teacherClasses]);

  useEffect(() => {
    if (preparedSuccess) {
      setOpen(true);

      setTimeout(() => {
        setOpen(false);
      }, 2000);
    }
  }, [preparedSuccess]);

  const [buttonText, setBttonText] = useState(BUTTON_TEXT_SEND_ISSUE);

  function makeInitialClassList(teacherClasses: SchoolClasses[]) {
    const schoolClass = teacherClasses.map((element) =>
      String(element.initials.number + element.initials.literal)
    );
    dispatch(fillAvailableClasses({ classList: schoolClass }));
  }

  function handlerSendApplication() {
    if (buttonText == BUTTON_TEXT_SEND_ISSUE) {
      setBttonText(BUTTON_TEXT_SAVED_CHANGED);
    } else if (buttonText == BUTTON_TEXT_SAVED_CHANGED) {
      prepare({
        class_id: сlassID,
        on_date: dataCh,
        overriden_pupils: prepareItemsArray,
      });
    }
  }

  return (
    <div className='containerTeacherMain'>
      <HeaderTeacherWidget
        name={currentUser?.firstName + ' ' + currentUser?.lastName}
      />
      <div className='containerTeacherApplyApplication'>
        <div className='title'>
          <div className='titleText'>Подать заявку</div>
          <div
            className={
              planReportStatus == 'Не подана' ? 'status' : 'status status__done'
            }
          >
            {planReportStatus}
          </div>
        </div>
        <div className='message'>{infoMessageTime}</div>
        <div className='containerTeacherApplication'>
          <div className='containerClassSelection'>
            <div className='headerTable'>
              <ClassSelection />
              <MonthSelection />
            </div>
          </div>
          <Table />
          <div className='btnWrapper'>
            {/* {buttonText == BUTTON_TEXT_SAVED_CHANGED && (
              <button
                className='btn btnCancelChange'
                onClick={handlerCancelChange}
              >
                Отменить
              </button>
            )} */}
            <button
              className='btn btnSendAppl'
              onClick={handlerSendApplication}
            >
              {buttonText}
            </button>
            <Popup nested modal open={open}>
              {() => <div className='modalText'>Заявка успешно отправлена</div>}
            </Popup>
          </div>
        </div>
      </div>
    </div>
  );
}
