import {LimitedFieldData} from '../types/limited-field-data';

export type ModalLimitedFieldProps = {
  symbolLimit: number,
  buttonTitle: string,
  onSubmit: (currentData: LimitedFieldData) => void
};
