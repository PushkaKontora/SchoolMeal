import {Toast} from 'react-native-toast-notifications';
import {ToastPayload} from '../../ui/special/toast/model/props';

export class ToastService {
  public hideAll() {
    Toast.hideAll();
  }

  public show(type: string, data: ToastPayload) {
    this.hideAll();
    Toast.show('', {
      type: type,
      data: data
    });
  }
}
