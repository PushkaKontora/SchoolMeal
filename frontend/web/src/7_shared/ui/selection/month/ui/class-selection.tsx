import '../consts/style.scss';
import leftArrow from '../assets/images/leftArrow.jpg';
import rightArrow from '../assets/images/rightArrow.jpg';

export default function MonthSelection() {
  return (
    <div className='date'>
      <img src={leftArrow} alt='this is top image' />
      <div className='text'>среда 15.05</div>
      <img src={rightArrow} alt='this is top image' />
    </div>
  );
}
