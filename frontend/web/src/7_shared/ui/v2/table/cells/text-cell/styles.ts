import styled from 'styled-components';
import {CSSProperties} from 'react';

export const Container = styled.div<{
  $header?: boolean;
  $justifyContent?: CSSProperties['justifyContent'];
  $padding?: CSSProperties['padding'];
}>`
  display: flex;
  justify-content: ${props => props.$justifyContent || 'flex-start'};
  align-items: center;
  
  padding: ${props => props.$padding || '0px 12px 0px 12px'};
  
  font-weight: ${props => props.$header ? '500' : '400'};
  font-size: 14px;
  line-height: 22px;
`;
