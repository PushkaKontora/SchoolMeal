import styled, {css} from 'styled-components';

const SWITCH_WIDTH = '37.14px';
const SWITCH_TOGGLE_WIDTH = '15.71px';
const SWITCH_PADDING = '2.14px';
const TRANSLATE_DISTANCE =
  css`calc(${SWITCH_WIDTH} - 2 * ${SWITCH_PADDING} - ${SWITCH_TOGGLE_WIDTH})`;

export const SwitchLabel = styled.label`
  position: relative;
  display: inline-block;

  width: ${SWITCH_WIDTH};
  height: 20px;
`;

export const SwitchInput = styled.input`
  opacity: 0;
  width: 0;
  height: 0;
`;

export const SwitchToggle = styled.div<{
  $toggled: boolean,
  $disabled?: boolean
}>`
  display: inline;

  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  -webkit-transition: .4s;
  transition: .4s;

  border-radius: 50px;

  opacity: ${props => props.$disabled ? 0.25 : 1};

  background-color: ${props => props.$toggled ? '#2C2C2C' : '#E9E9E9'};

  input:disabled ~ & {
    cursor: default;

    background-color: #ff5f5f;
  }

  &:before {
    position: absolute;
    content: "";

    width: ${SWITCH_TOGGLE_WIDTH};
    height: ${SWITCH_TOGGLE_WIDTH};

    border-radius: 50%;

    left: ${SWITCH_PADDING};
    bottom: ${SWITCH_PADDING};
    background-color: white;
    box-shadow: 0 0.5px 2.12px rgba(0, 0, 0, 0.25);
    -webkit-transition: .4s;
    transition: .4s;

    ${props => {
      if (props.$toggled) {
        return css`
          -ms-transform: translateX(${TRANSLATE_DISTANCE});
          transform: translateX(${TRANSLATE_DISTANCE});
        `;
      }
    }}
  }
`;
