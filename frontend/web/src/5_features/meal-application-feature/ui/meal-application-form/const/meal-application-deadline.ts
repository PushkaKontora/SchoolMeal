export const MealApplicationDeadline = () => {
  const today = new Date();

  today.setHours(23, 0, 0, 0);

  return today;
};
