import styled from 'styled-components';
import {DEFAULT_STYLES} from './default-styles.ts';

export const SidebarContainer = styled.section`
  ${{...DEFAULT_STYLES}}
`;

export const SidebarItemList = styled.nav`
  margin-top: 32px;
  
  display: flex;
  flex-direction: column;
  
  width: 100%;
  
  flex: 1;
  
  gap: 8px;
`;

export const SidebarBottomActions = styled.section`
  margin-top: 32px;

  display: flex;
  flex-direction: column;

  width: 100%;
`;
