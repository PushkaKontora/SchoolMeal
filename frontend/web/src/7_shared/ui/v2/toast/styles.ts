import styled from 'styled-components';

export const ToastStyles = styled.div`
  border: 1px solid #48C1B5;
  background-color: #F6FFF9;
  border-radius: 12px;
  
  padding: 20px;
  
  display: flex;
  flex-direction: row;
  gap: 16px;
`;

export const ToastText = styled.div`
  font-family: 'Ubuntu', sans-serif;
  font-size: 14px;
  font-weight: 700;
  
  line-height: 19.6px;
  
  color: #27303A;
`;

export const CloseButtonStyles = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;

  width: 18px;
  height: 18px;
  
  padding: 0;
  margin: 0;
  
  border: none;
  background-color: #00000000;
`;
