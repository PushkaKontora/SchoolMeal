import '../consts/style.scss';
import logo from '../../../../7_shared/assets/images/logo.jpg';

export default function HeaderTeacherWidget(props: { name: string }) {
  const { name } = props;

  return (
    <div className='containerHeaderTeacher'>
      <div className='navigations navigations__left'>
        <div className='logo'>
          <img src={logo} alt='this is top image' />
        </div>
        <div className='navigateItems'>
          <div className='item'>Список класса</div>
          <div className='item item__active'>Подать заявку</div>
          <div className='item'>История заявок</div>
        </div>
      </div>
      <div className='navigations'>
        <div className='name'>{name}</div>
        <div className='buttonExit'>Выйти</div>
      </div>
    </div>
  );
}
