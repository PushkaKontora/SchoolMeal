import {LogoContainer} from './styles.ts';
import logo from '../assets/logo.png';

export function Logo() {
  return (
    <LogoContainer
      src={logo}
      alt={'SchoolMeal'}/>
  );
}
