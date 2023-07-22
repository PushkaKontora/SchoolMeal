export type ValueBadgeStyles = {
  backgroundColor?: string,
  textColor?: string,
  width?: string
}

export type ValueBadgeProps = {
  value: string
} & ValueBadgeStyles;
