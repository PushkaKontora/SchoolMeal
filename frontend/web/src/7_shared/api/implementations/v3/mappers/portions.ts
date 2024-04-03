import {
  MealtimePortionsOut,
  PortionsReportResponse,
  SchoolClassWithPortionsOut
} from '../backend-types/nutrition/portions.ts';
import {MealtimePortions, PortionsReport, SchoolClassWithPortions} from '../frontend-types/nutrition/portions.ts';
import {Mealtime} from '../frontend-types/nutrition/mealtime.ts';
import {MealtimeOut} from '../backend-types/nutrition/mealtime.ts';

export const toMealtimePortions = (portions: MealtimePortionsOut): MealtimePortions => {
  const result: MealtimePortions = {};

  Object.keys(portions).forEach(mealtime => {
    const mt = mealtime as MealtimeOut;
    result[Mealtime[mt]] = portions[mt];
  });

  return result;
};

export const toSchoolClassWithPortions = (schoolClass: SchoolClassWithPortionsOut): SchoolClassWithPortions => ({
  id: schoolClass.id,
  number: schoolClass.number,
  literal: schoolClass.literal,
  portions: toMealtimePortions(schoolClass.portions)
});

export const toSchoolClassWithPortionsArray = (schoolClasses: SchoolClassWithPortionsOut[]) =>
  schoolClasses.map(toSchoolClassWithPortions);

export const toPortionsReport = (report: PortionsReportResponse): PortionsReport => ({
  schoolClasses: toSchoolClassWithPortionsArray(report.schoolClasses),
  totals: toMealtimePortions(report.totals)
});

export const toPortionsReportArray = (reports: PortionsReportResponse[]): PortionsReport[] =>
  reports.map(toPortionsReport);
