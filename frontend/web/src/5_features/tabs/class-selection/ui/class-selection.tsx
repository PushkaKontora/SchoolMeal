import '../consts/style.scss';
import ClassItemWidget from '../../../../4_widgets/teacher-blocks/class-item/ui/class-item';
import { useAppSelector } from '../../../../../store/hooks';

export default function ClassSelection() {
  const classList = useAppSelector((state) => state.classTabs.classList);

  return (
    <div className='containerClassItems'>
      {classList.map((item, index) => (
        <ClassItemWidget key={item} className={item} indexArray={index} />
      ))}
    </div>
  );
}
