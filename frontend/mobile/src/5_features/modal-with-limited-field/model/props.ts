import {FeedbackFormProps} from '../../../6_entities/feedback/ui/feedback-form';

export type FeedbackModalProps = FeedbackFormProps & {
  title: string,
  successfulSubmission: boolean,
  successComponent: JSX.Element
};
