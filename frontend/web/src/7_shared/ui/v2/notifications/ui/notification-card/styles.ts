import styled from 'styled-components';

export const Card = styled.article<{
  $read?: boolean
}>`
  background-color: ${props => props.$read ? '#00000000' : '#333333'};
  padding: 16px;
  
  border-radius: 8px;
  
  display: flex;
  flex-direction: column;
`;

export const Name = styled.div`
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 16px;
  
  color: #FFF;
  
  line-height: 19.2px;
  
  margin-bottom: 4px;
`;

export const Reason = styled.div`
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 14px;
  
  color: #E9632C;
  
  line-height: 16.8px;
  
  margin-bottom: 6px;
`;

export const Description = styled.div`
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 14px;
  
  color: #C5C5C5;
  
  line-height: 16.8px;
`;
