import styled from 'styled-components';

export const InputFieldContainer = styled.input`
  padding: 0 20px;

  width: 100%;
  height: 56px;

  background: #FFFFFF;

  border: 1px solid #9C9C9C;
  border-radius: 10px;
  
  &:active {
    border-color: #4AC1FF;
  }
  
  &::placeholder {
    color: #B1B1B1
  }
`;
