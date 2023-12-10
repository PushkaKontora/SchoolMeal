import '../consts/style.scss';
import HeaderTeacherWidget from '../../../4_widgets/header-teacher/ui/header-teacher.tsx';
import { infoMessageTime, infoMessageInstruction } from '../consts/consts.ts';
import { useState } from 'react';
import Popup from 'reactjs-popup';
import ClassSelection from '../../../5_features/tabs/class-selection/ui/class-selection.tsx';
import MonthSelection from '../../../7_shared/ui/selection/month/ui/class-selection.tsx';
import Table from '../../../5_features/table/table/ui/table.tsx';

export function TeacherMainPage() {
  const [open, setOpen] = useState(false);

  const statusName = 'Не подана';

  function handlerSendApplication() {
    setOpen(true);

    setTimeout(() => {
      setOpen(false);
    }, 2000);
  }

  return (
    <div className='containerTeacherMain'>
      <HeaderTeacherWidget />
      <div className='containerTeacherApplyApplication'>
        <div className='title'>
          <div className='titleText'>Подать заявку</div>
          <div
            className={
              statusName == 'Не подана' ? 'status' : 'status status__done'
            }
          >
            {statusName}
          </div>
        </div>
        <div className='message'>
          {infoMessageTime} <br /> {infoMessageInstruction}
        </div>
        <div className='containerTeacherApplication'>
          <div className='containerClassSelection'>
            <div className='headerTable'>
              <ClassSelection />
              <MonthSelection />
            </div>
          </div>
          <Table/>
          <div className='btnSendAppl'>
            <button className='btn' onClick={handlerSendApplication}>
              Отправить заявку
            </button>
            <Popup nested modal open={open}>
              {() => (
                <div className={'modalText'}>Заявка успешно отправлена</div>
              )}
            </Popup>
          </div>
        </div>
      </div>
    </div>
  );
}
