export type ToggleButtonProps = {
  leftTitle: string,
  rightTitle: string,
  onToggle: (toggledRight: boolean) => void,
  defaultState?: boolean
};
