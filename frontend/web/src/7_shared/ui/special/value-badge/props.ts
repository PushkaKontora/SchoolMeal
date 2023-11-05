export type ValueBadgeStyles = {
  backgroundColor?: string,
  textColor?: string,
  width?: string,
  margin?: string
}

export type ValueBadgeProps = {
  value: string
} & ValueBadgeStyles;
