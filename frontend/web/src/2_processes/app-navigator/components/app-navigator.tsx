import {LoadingPage} from '../../../3_pages/loading-page';
import {BrowserRouter} from 'react-router-dom';
import {AppRouter} from '../../routers/app-router';
import {useAppSelector} from '../../../../store/hooks';
import {AuthController} from '../../auth-controller';
import { TeacherMainPage } from '../../../3_pages/teacher-main-page/ui/teacher-main-page';

export function AppNavigator() {
  const authorized = useAppSelector((state) => state.auth.authorized);

  return (
    <BrowserRouter>
    <TeacherMainPage/>
      {/* <AuthController/>
      {
        authorized === undefined && (
          <LoadingPage/>
        )
      }
      <AppRouter/> */} 
    </BrowserRouter>
  );
}

