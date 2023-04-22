import {generateStack} from '../../../7_shared/lib/stack-creator';
import {SCREEN_OPTIONS, SCREENS} from './config/config';

export default () => generateStack(SCREENS, SCREEN_OPTIONS);
