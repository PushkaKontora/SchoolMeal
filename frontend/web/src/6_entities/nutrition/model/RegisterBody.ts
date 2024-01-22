export type RegisterBody = {
  class_id: string;
  on_date: string;
  overriden_pupils: OverridenPupil[];
};

export type OverridenPupil = {
  id: string;
  breakfast: boolean;
  dinner: boolean;
  snacks: boolean;
};
