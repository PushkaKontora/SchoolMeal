import {SidebarIconedButtonProps} from './props.ts';
import {SidebarIconedButtonContainer, SidebarIconedButtonText} from './styles.ts';

export function SidebarIconedButton(props: SidebarIconedButtonProps) {
  return (
    <SidebarIconedButtonContainer
      onClick={props.onClick}
      active={props.active}>
      {
        props?.icon
      }
      <SidebarIconedButtonText>
        <div>
          {props.text}
        </div>
        {props.children}
      </SidebarIconedButtonText>
    </SidebarIconedButtonContainer>
  );
}
