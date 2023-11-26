import {PropsWithChildren} from 'react';
import {FeedbackData} from '../../../../../6_entities/feedback';

export type MenuProps = {
    schoolId: string,
} & PropsWithChildren;

export type MenuFeedbackModalProps = Pick<FeedbackData, 'canteenId'>;
