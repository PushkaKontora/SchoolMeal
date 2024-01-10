export type ModalMealPeriodProps = {
  initialDate?: Date,
  passedDatesUntil?: Date,
  onConfirm: (startingDate: Date, endingDate: Date) => void,
  onClose: () => void
};
