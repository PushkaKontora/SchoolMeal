import styled from 'styled-components';

export const BadgeContainer = styled.div<{
  $backgroundColor?: string,
  $textColor?: string,
  $margin?: string,
  $fontFamily?: string,
  $width?: string
}>`
  background-color: ${props => props.$backgroundColor || '#F6F6F6'};
  color: ${props => props.$textColor || '#2C2C2C'};
  margin: ${props => props.$margin || 0};
  
  font-family: ${props => props.$fontFamily || 'inherit'}, sans-serif;
  font-weight: 500;
  font-size: 14px;
  text-align: center;
  vertical-align: middle;
  padding: 4px 8px;
  
  border-radius: 4px;
  width: ${props => props.$width || 'auto'};

  display: inline-block;
`;
