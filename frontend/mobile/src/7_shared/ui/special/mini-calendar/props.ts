export type MiniCalendarProps = {
  selectionColor: string,
  currentDate?: Date,
  itemNumber?: number
};

export type DateButtonProps = {
  date: Date,
  checked?: boolean,
  selectionColor: string,
  onPress: () => void
}
