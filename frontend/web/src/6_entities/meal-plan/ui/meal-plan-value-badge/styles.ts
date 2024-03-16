import styled from 'styled-components';
import {CSSProperties} from 'react';

export const Container = styled.div<{
  $justifyContent?: CSSProperties['justifyContent'];
  $padding?: CSSProperties['padding'];
}>`
  display: flex;
  justify-content: ${props => props.$justifyContent || 'flex-start'};
  align-items: center;
  
  padding: ${props => props.$padding || '0px 12px 0px 12px'};
`;
