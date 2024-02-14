import styled from 'styled-components';
import {CSSProperties} from 'react';

export const ParentContainer = styled.div<{
  $sidebarWidth: string
}>`
  width: 100%;
  height: 100%;
  
  display: flex;
  flex-direction: row;
  
  position: relative;
`;

export const Content = styled.div<{
  $sidebarWidth: string
}>`
  width: calc(100% - ${props => props.$sidebarWidth});
  height: 100%;
  
  flex: 1;
  padding-left: ${props => props.$sidebarWidth};
`;

export const ContentBody = styled.div<{
  $padding: CSSProperties['padding']
}>`
  padding: ${props => props.$padding};
`;
