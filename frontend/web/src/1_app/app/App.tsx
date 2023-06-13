import '../styles/App.css'
import {Provider} from 'react-redux';
import {store} from '../../../store/store';
import {AppNavigator} from '../../2_processes/app-navigator';
import {TeacherMainPage} from "../../3_pages/teacher-main-page/ui/teacher-main-page.tsx";

function App() {

  return (
    <Provider store={store}>
      <AppNavigator/>
    </Provider>
  )
}

export default App
