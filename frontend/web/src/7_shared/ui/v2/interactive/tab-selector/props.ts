export type TabSelectorProps = {
  selected: number,
  tabs: {
    name: string,
    onClick: () => void
  }[]
}
