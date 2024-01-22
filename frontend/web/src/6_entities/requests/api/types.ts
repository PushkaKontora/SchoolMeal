import {RequestReportSchoolClass} from '../../../7_shared/model/request-report.ts';

export type RequestReportIn = {
  classType: 'primary' | 'high',
  date: string
};

export type RequestReport = {
  school_classes: RequestReportSchoolClass[],
  paid_total: number,
  preferential_total: number,
  total: number
};
