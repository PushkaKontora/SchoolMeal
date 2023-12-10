import { useAppDispatch, useAppSelector } from '../../../../../store/hooks.ts';
import '../consts/style.scss';
import { ClassItemProps } from '../model/props.ts';
import { selectionClassTabs } from '../../../../5_features/tabs/class-selection/model/class-tabs-slice.ts';

export default function ClassItemWidget(props: ClassItemProps) {
  const { className } = props;

  const activeClass = useAppSelector((state) => state.classTabs.activeClass);
  const dispatch = useAppDispatch();

  function handlerChooseClass() {
    dispatch(selectionClassTabs({ activeClass: className }));
  }

  return (
    <div
      className={
        activeClass != className ? 'className' : 'className className__active'
      }
      onClick={handlerChooseClass}
    >
      {className}
    </div>
  );
}
