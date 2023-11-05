import '../consts/style.scss';
import ClassItemWidget from '../../../../4_widgets/teacher-blocks/class-item/ui/class-item';

export default function ClassSelection() {
  const classArray = ['1А', '2Б'];

  return (
    <div className='containerClassItems'>
      {classArray.map((item) => (
        <ClassItemWidget key={item} className={item} />
      ))}
    </div>
  );
}
