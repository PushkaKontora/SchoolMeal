export type CallbackFunction = (action: any) => void;

export class Listeners {
  readonly callbacks: Array<CallbackFunction> = [];

  addCallback(func: CallbackFunction) {
    this.callbacks.push(func);
  }

  emit(action: any) {
    this.callbacks.forEach(func => func(action));
  }
}

export class MiddlewareListeners {
  readonly onSuccessListeners: Listeners = new Listeners();
  readonly onRejectedListeners: Listeners = new Listeners();

  addSuccessCallback(f: CallbackFunction) {
    this.onSuccessListeners.addCallback(f);
  }

  addRejectedCallback(f: CallbackFunction) {
    this.onRejectedListeners.addCallback(f);
  }

  emitSuccess(action: any) {
    this.onSuccessListeners.emit(action);
  }

  emitRejection(action: any) {
    this.onRejectedListeners.emit(action);
  }
}
