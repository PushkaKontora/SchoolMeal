import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
`;

export const Title = styled.div`
  font-size: 14px;
  font-weight: 400;
  
  line-height: 22px;
  
  white-space: nowrap;
`;

export const Status = styled.div<{
  $color: string
}>`
  font-size: 20px;
  font-weight: 600;

  line-height: 30px;
  
  color: ${props => props.$color};

  white-space: nowrap;
`;
