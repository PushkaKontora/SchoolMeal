import styled from 'styled-components';

export const Container = styled.div<{
  $header: boolean;
  $justifyContent?: string;
  $padding?: string;
}>`
  display: flex;
  justify-content: ${props => props.$justifyContent || 'flex-start'};
  align-items: center;
  
  padding: ${props => props.$padding || '0px 12px 0px 12px'};
  
  font-weight: ${props => props.$header ? '500' : '400'};
  font-size: 14px;
  line-height: 22px;
`;
