import {LimitedFieldData} from '../types/limited-field-data';

export type FeedbackModalProps = ModalLimitedFieldProps & {
  successfulSubmission: boolean
};

export type ModalLimitedFieldProps = {
  symbolLimit: number,
  buttonTitle: string,
  onSubmit: (currentData: LimitedFieldData) => void
};
