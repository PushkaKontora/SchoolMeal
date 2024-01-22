export type RequestReportSchoolClass = {
  id: string,
  initials: string,
  breakfast: RequestReportMealInfo,
  dinner: RequestReportMealInfo,
  snacks: RequestReportMealInfo
};

export type RequestReportMealInfo = {
  paid: number,
  preferential: number,
  total: number
};
