import {CSSProperties} from 'react';
import {SIDEBAR_WIDTH} from '../../config/config.ts';

export const DEFAULT_STYLES: CSSProperties = {
  backgroundColor: '#2C2C2C',
  borderRadius: '0px 16px 16px 0px',
  padding: '40px 18px 48px 18px',

  width: SIDEBAR_WIDTH,
  height: '100%',

  position: 'fixed',
  boxSizing: 'border-box',

  display: 'flex',
  flexDirection: 'column',

  fontFamily: 'Inter',

  zIndex: 100,
};
