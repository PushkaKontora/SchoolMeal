export const MealApplicationDeadline = () => {
  const today = new Date();

  today.setHours(19, 0, 0, 0);

  return today;
};
