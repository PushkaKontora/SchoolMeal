export type ModalMealPeriodProps = {
  initialDate?: Date,
  onConfirm: (startingDate: Date, endingDate: Date) => void,
  onClose: () => void
};
