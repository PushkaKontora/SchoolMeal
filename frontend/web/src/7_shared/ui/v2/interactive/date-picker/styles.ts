import styled from 'styled-components';
import {CSSProperties} from 'react';

export const Container = styled.div<{
  $width: CSSProperties['width']
}>`
  width: ${props => props.$width || '310px'};
  height: 40px;
  
  display: flex;
  flex-direction: row;
  box-sizing: border-box;
  
  justify-content: space-around;
  align-items: center;
  padding: 8px 12px;
  
  background-color: #F5F5F5;
`;

export const ArrowButton = styled.button`
  width: 26px;
  height: 26px;

  display: flex;
  align-items: center;
  justify-content: center;

  background-color: #2C2C2C;
  border-radius: 50%;

  transition: background-color 1s;

  &:hover {
    background-color: #181818;
  }

  &:active {
    background-color: #050505;
  }
`;

export const DateTitle = styled.div`
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;
  
  text-transform: capitalize;
`;
