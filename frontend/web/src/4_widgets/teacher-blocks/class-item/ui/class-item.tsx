import { useAppDispatch, useAppSelector } from '../../../../../store/hooks.ts';
import '../consts/style.scss';
import { ClassItemProps } from '../model/props.ts';
import { selectionClassTabs } from '../../../../5_features/tabs/class-selection/model/class-tabs-slice.ts';

export default function ClassItemWidget(props: ClassItemProps) {
  const { className, indexArray } = props;

  const activeClass = useAppSelector((state) => state.classTabs.activeClass);
  const allTeacherClasses = useAppSelector(
    (state) => state.classTabs.allClassList
  );
  const dispatch = useAppDispatch();

  function handlerChooseClass() {
    dispatch(
      selectionClassTabs({
        activeClass: className,
        classID: allTeacherClasses[indexArray].id,
      })
    );
    console.log(indexArray, allTeacherClasses[indexArray].id, '4');
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
