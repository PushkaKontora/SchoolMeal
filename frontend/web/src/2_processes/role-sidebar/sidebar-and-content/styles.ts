import styled from 'styled-components';

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
  
  position: absolute;
  right: 0;
`;
