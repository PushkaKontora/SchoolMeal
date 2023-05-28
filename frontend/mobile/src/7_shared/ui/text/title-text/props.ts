import {FlexAlignType} from "react-native";
import {PropsWithChildren} from "react";

export type TitleTextProps = {
    title: string,
    textColor?: string,
    lineHeight?: number,
    fontSize?: number,
    fontWeight?: "bold" | "100" | "600" | "normal" | "200" | "300" | "400" | "500" | "700" | "800" | "900" | undefined,
    paddingBottom?: number,
    alignItems?: FlexAlignType | undefined,
    marginLeft?: string | number,
} & PropsWithChildren;
