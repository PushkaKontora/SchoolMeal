import styled, {css} from 'styled-components';

export const SidebarIconedButtonContainer = styled.article<{
  active?: boolean
}>`
  height: 52.5px;
  padding: 0 16px;
  border-radius: 8px;
  
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  
  gap: 16px;
  
  background-color: ${props => props.active ? '#171717' : '#00000000'};
  
  ${props => {
    if (!props.active) {
      return css`
        &:hover {
          background-color: rgba(23, 23, 23, 0.5);
        }
      `;
    }
  }}
`;

export const SidebarIconedButtonText = styled.div`
  font-weight: 600;
  font-size: 16px;
  line-height: 19px;
  
  color: #9E9E9E;
  
  flex: 1;
`;
