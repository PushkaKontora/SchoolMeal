import styled from 'styled-components';

export const Row = styled.tr`
  width: 100%;
`;

export const Cell = styled.td<{
  $width: string,
  $minWidth: string,
  $maxWidth: string,
  $header: boolean,
  $backgroundColor: string,
  $fontFamily: string,
  $height: string
}>`
  width: ${props => props.$width || 'auto'};
  min-width: ${props => props.$minWidth || 0};
  max-width: ${props => props.$maxWidth || 'none'};
  
  height: ${props => props.$height || '50px'};
  
  background-color: ${props => props.$backgroundColor || (props.$header ? '#F5F5F5' : '#00000000')};
  font-family: ${props => props.$fontFamily || 'inherit'};
  border-bottom: 1px solid #EAEAEA;
`;
