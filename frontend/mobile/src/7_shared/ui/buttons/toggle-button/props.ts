export type ToggleButtonProps = {
  turnedOffTitle: string,
  turnedOnTitle: string,
  onToggle: (turnedOn: boolean) => void,
  defaultState?: boolean
};
