import styled from 'styled-components';

export const TableContainer = styled.table<{
  $width?: string
}>`
  width: ${props => props.$width || '100%'};
  
  border-collapse: collapse;
  
  overflow-y: auto;
`;
