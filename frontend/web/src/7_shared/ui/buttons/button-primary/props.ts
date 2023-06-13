export type ButtonPrimaryStyles = {
    borderRadius?: string,
    backgroundColor?: string
    textColor?: string,
    fontSize?: string,
    paddingVertical?: string,
    paddingHorizontal?: string
}

export type ButtonPrimaryProps =
  ButtonPrimaryStyles & {
    title: string,
    onPress: () => void,
    disabled?: boolean,
  };
