import {isRejectedWithValue, Middleware, PayloadAction} from '@reduxjs/toolkit';
import {ToastService} from '../../../../7_shared/lib/toast-service';

//export const callbacks: MiddlewareListeners = new MiddlewareListeners();

export const errorHandlerMiddleware: Middleware =
  () => (next) => <A extends PayloadAction<{
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

    return next(action);
  };

export default {errorHandlerMiddleware};
