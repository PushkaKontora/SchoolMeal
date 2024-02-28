import styled from 'styled-components';
import {CSSProperties} from 'react';

export const Container = styled.div<{
  $justifyContent: CSSProperties['justifyContent']
}>`
  height: 100%;
  
  display: flex;
  justify-content: ${props => props.$justifyContent || 'center'};
  align-items: center;
  
  gap: 12px;
`;
