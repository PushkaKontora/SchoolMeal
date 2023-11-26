export {};

declare global {
  namespace SchoolMeal {
    interface ProcessEnv {
      HMAC_KEY_NAME: string;
    }

    declare module '*.svg' {
      import React from 'react';
      import { SvgProps } from 'react-native-svg';
      const content: React.FC<SvgProps>;
      export default content;
    }
  }
}
