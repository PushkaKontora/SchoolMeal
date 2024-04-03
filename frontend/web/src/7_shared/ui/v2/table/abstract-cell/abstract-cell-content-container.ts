import styled from 'styled-components';
import {CSSProperties} from 'react';

export const ContentContainer = styled.div<{
  $justifyContent?: CSSProperties['justifyContent'];
  $padding?: CSSProperties['padding'];
  $alignItems?: CSSProperties['alignItems']
}>`
  display: flex;
  justify-content: ${props => props.$justifyContent || 'flex-start'};
  align-items: ${props => props.$alignItems || 'center'};
  
  padding: ${props => props.$padding || '0px 12px 0px 12px'};
`;
