export const MealApplicationDeadline = () => {
  const today = new Date();

  today.setHours(22, 0, 0, 0);

  return today;
};
