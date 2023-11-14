import {isFulfilled, isRejectedWithValue, Middleware, MiddlewareAPI} from '@reduxjs/toolkit';
import {MiddlewareListeners} from './types';
import {Toast} from 'react-native-toast-notifications';

//export const callbacks: MiddlewareListeners = new MiddlewareListeners();

export const errorHandlerMiddleware: Middleware =
  (api: MiddlewareAPI) => (next) => (action) => {
    if (isRejectedWithValue(action)) {
      Toast.show('fdfdsfsdds', {
        type: 'danger',
        data: {
          title: action.payload.data.detail
        }
      });
    }

    /*
    if (isFulfilled(action)) {
      callbacks.emitRejection(action);
    }
    */

    return next(action);
  };

export default {errorHandlerMiddleware};
