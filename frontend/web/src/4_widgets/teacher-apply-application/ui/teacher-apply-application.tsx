import '../consts/style.scss';
import {TeacherApplyApplicationProps} from '../model/props.ts';
import TeacherApplicationPersonal
  from '../../../5_features/teacher-application-personal/ui/teacher-application-personal.tsx';

export default function TeacherApplyApplicationWidget(props: TeacherApplyApplicationProps) {

  return (
    <div className='containerTeacherApplyApplication'>
      <div className="title">
        <div className="titleText">
                    Подать заявку
        </div>
        <div className={props.statusName == 'Не подана' ? 'status' : 'status status__done'}>
          {props.statusName}
        </div>
      </div>
      <div className="message">
                Подайте заявку на завтра до 15:00, в 15:00 система отправит заявку атоматически.<br/>
                При необходимости вы сможете редактировать заявку до 10:00 застрашнего дня.
      </div>
      <TeacherApplicationPersonal/>
    </div>
  );
}

