import React from "react";

export type ScreenInfo = {
  component: React.ComponentType,
  options?: any
};

export type ScreenConfig = {
  [index: string]: ScreenInfo
};
