import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  min-width: 300px;
  
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  
  align-items: center;
`;

export const Tab = styled.button<{
  $selected: boolean,
}>`
  padding: 8px 16px;
  border-radius: 100px;
  border: none;
  
  font-size: 16px;
  font-weight: ${props => props.$selected ? '700' : '400'};
  
  background-color: ${props => props.$selected ? '#2C2C2C' : '#F5F5F5'};
  color: ${props => props.$selected ? '#FFFFFF' : '#141414'};
`;
