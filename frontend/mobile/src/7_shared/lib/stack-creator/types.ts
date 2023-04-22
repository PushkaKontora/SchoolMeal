import React from 'react';

export type ScreenInfo = {
  component: React.ComponentType<any>,
  options?: any
};

export type ScreenConfig = {
  [index: string]: ScreenInfo
};

