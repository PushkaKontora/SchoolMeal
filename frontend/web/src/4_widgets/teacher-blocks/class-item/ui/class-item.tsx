import '../consts/style.scss';
import {ClassItemProps} from '../model/props.ts';

export default function ClassItemWidget(props: ClassItemProps) {
  const active = '1А';

  return (
    <div className={active != props.className ? 'className' : 'className className__active'}>
      {props.className}
    </div>
  );
}

