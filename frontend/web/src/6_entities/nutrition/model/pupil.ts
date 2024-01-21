export type SchoolClasses = {
  id: string;
  lastName: string;
  firstName: string;
  mealPlan: {
    hasBreakfast: boolean;
    hasDinner: boolean;
    hasSnacks: boolean;
  };
  preferentialCertificate: {
    endsAt: string;
  };
  cancellationPeriods: [
    {
      startsAt: string;
      endsAt: string;
      reasons: string[];
    }
  ];
  status: string;
};
