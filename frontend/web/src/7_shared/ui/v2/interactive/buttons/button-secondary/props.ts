export type ButtonSecondaryStyles = {
  borderRadius?: string,
  backgroundColor?: string
  textColor?: string,
  fontSize?: string,
  paddingVertical?: string,
  paddingHorizontal?: string
}

export type ButtonSecondaryProps =
  ButtonSecondaryStyles & {
  title: string,
  onPress: () => void,
  disabled?: boolean,
};