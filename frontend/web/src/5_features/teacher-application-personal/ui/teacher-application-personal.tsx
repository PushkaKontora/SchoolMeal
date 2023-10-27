import '../consts/style.scss';
import ClassSelectionWidget from '../../../4_widgets/teacher-blocks/class-selection/ui/class-selection.tsx';
import TableWidget from '../../../4_widgets/teacher-blocks/table/ui/table.tsx';
import Popup from 'reactjs-popup';
import {useState} from 'react';

export default function TeacherApplicationPersonal() {
  const [open, setOpen] = useState(false);

  function handleSendApplication() {
    setOpen(true);

    setTimeout(() => {
      setOpen(false);
    }, 2000);
  }

  return (
    <div className="containerTeacherApplication">
      <ClassSelectionWidget/>
      <TableWidget/>
      <div className='btnSendAppl'>
        <button className='btn'
          onClick={handleSendApplication}
        >Отправить заявку
        </button>
        <Popup nested
          modal
          open={open}
        >
          {() => (
            <div className={'modalText'}>Заявка успешно отправлена</div>
          )}
        </Popup>
      </div>
    </div>
  );
}
