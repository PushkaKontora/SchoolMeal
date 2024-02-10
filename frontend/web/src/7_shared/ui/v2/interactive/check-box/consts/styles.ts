import styled from 'styled-components';

export const CheckboxLabel = styled.label`
  width: 20px;
  height: 20px;
  
  display: block;
`;

export const CheckboxContainer = styled.div<{
  $checked: boolean,
  $disabled: boolean
}>`
  width: 100%;
  height: 100%;

  position: relative;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  box-sizing: border-box;

  border: 1px solid #2C2C2C;
  border-radius: 2px;

  background-color: ${props => props.$checked ? '#2C2C2C' : '#00000000'};

  opacity: ${props => props.$disabled ? 0.5 : 1};
`;

export const CheckboxInput = styled.input.attrs(() => ({
  type: 'checkbox'
}))`
  -webkit-appearance: none;
  appearance: none;
  
  position: absolute;
`;
