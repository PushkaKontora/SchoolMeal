export type PlanReport = {
  class_id: string;
  on_date: string;
  status: string;
  pupils: PupilItemApi[];
};

export type PupilItemApi = {
  id: string;
  last_name: string;
  first_name: string;
  patronymic: string;
  breakfast: boolean;
  dinner: boolean;
  snacks: boolean;

};
