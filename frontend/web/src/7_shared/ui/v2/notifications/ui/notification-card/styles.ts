import styled from 'styled-components';

export const Card = styled.article<{
  $read?: boolean
}>`
  position: relative;
  
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

export const Mark = styled.div`
  position: absolute;
  right: 10px;
  top: 10px;
  
  width: 32px;
  height: 32px;
  
  background-color: #FFFFFF;
  border-radius: 50%;
  
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 16px;
  color: #171717;
  
  text-align: center;
  vertical-align: middle;
  
  line-height: 30px;
`;
