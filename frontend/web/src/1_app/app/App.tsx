import '../styles/App.css'
import {Provider} from 'react-redux';
import {store} from '../../../store/store';
import {AppNavigator} from '../../2_processes/app-navigator';

function App() {
  return (
    <Provider store={store}>
      <AppNavigator/>
    </Provider>
  )
}

export default App
