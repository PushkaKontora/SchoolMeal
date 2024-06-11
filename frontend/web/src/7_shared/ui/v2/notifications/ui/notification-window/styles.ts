import styled from 'styled-components';

export const CloseButton = styled.button`
  border: none;
  background-color: #00000000;

  width: 12px;
  height: 12px;

  padding: 0;
  margin: 6px 6px 0 0;
`;

export const NotificationWindowContainer = styled.div<{
  $hidden: boolean
}>`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  
  width: 400px;
  height: 550px;
  
  background-color: #171717;
  border-radius: 8px;
  
  position: fixed;
  left: 289px;
  bottom: 108px;
  
  transition: 0.4s;
  z-index: 1000;
  visibility: ${props => props.$hidden ? 'hidden' : 'visible'};
  opacity: ${props => props.$hidden ? 0 : 1};
`;

export const WindowBody = styled.section`
  width: calc(100% - 18px);
  flex: 1;

  overflow-y: scroll;

  display: flex;
  flex-direction: column;
  gap: 12px;

  margin-top: 8px;
  
  padding-bottom: 24px;
`;
