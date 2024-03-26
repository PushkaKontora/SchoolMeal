import '../styles/App.css';
import {Provider} from 'react-redux';
import {store} from '../../../store/store';
import {BrowserRouter} from 'react-router-dom';
import {AppBody} from './AppBody.tsx';

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <AppBody/>
      </BrowserRouter>
    </Provider>
  );
}

export default App;
