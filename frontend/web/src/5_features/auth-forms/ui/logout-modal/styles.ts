import styled from 'styled-components';

export const LogoutContainer = styled.div<{
  $hidden: boolean
}>`
  position: absolute;
  left: 0;
  right: 0;
  
  font-family: 'Roboto', sans-serif;
  
  background-color: rgba(39, 39, 39, 0.3);
  
  width: 100%;
  height: 100%;

  transition: 0.4s;
  z-index: 1000;
  visibility: ${props => props.$hidden ? 'hidden' : 'visible'};
  opacity: ${props => props.$hidden ? 0 : 1};
`;

export const LogoutWindow = styled.section`
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: flex-end;
  
  position: relative;
  top: 128px;
  margin: auto;
  
  opacity: 1;
  
  background-color: #FFFFFF;
  border-radius: 46px;
  
  padding: 40px 36px;
  
  width: 524px;
  box-sizing: border-box;
`;

export const LogoutWindowContent = styled.article`
  display: flex;
  flex-direction: column;
  gap: 32px;
  
  width: 100%;
`;

export const LogoutWindowMessage = styled.h1`
  font-weight: 600;
  font-size: 18px;
  line-height: 21.6px;
  
  text-align: center;
  
  color: #2C2C2C;
`;

export const LogoutButtons = styled.div`
  display: flex;
  gap: 8px;
  
  height: 40px;
`;
