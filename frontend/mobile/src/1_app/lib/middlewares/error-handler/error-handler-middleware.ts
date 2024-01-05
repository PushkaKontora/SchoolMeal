import {isRejectedWithValue, Middleware, MiddlewareAPI, PayloadAction} from '@reduxjs/toolkit';
import {ToastService} from '../../../../7_shared/ui/special/toast-notifier/toast-service';

//export const callbacks: MiddlewareListeners = new MiddlewareListeners();

export const errorHandlerMiddleware: Middleware =
  (api: MiddlewareAPI) => (next) => <A extends PayloadAction<{
    status: string,
    originalStatus: number,
    data: any,
    error: any
  }>>(action: A) => {
    if (isRejectedWithValue(action)) {
      ToastService.show('danger', {
        title: action.payload.originalStatus.toString(),
        description: action.payload.data
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
