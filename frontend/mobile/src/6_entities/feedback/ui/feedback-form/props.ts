import {FeedbackFormData} from './feedback-form-data';

export type FeedbackFormProps = {
  canteenId: string,
  symbolLimit?: number,
  buttonTitle: string,
  onSubmit: (currentData: FeedbackFormData) => void,
};
