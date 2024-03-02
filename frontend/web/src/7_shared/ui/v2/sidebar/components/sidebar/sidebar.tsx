import {SidebarBottomActions, SidebarContainer, SidebarItemList} from './styles.ts';
import {Logo} from '../logo/logo.tsx';
import {SidebarProps} from './props.ts';
import {SidebarIconedButton} from '../iconed-button/sidebar-iconed-button.tsx';
import {LogoutButton} from '../logout-button';

export function Sidebar(props: SidebarProps) {
  return (
    <SidebarContainer>
      <Logo/>
      <SidebarItemList>
        {props.items.map(item =>
          <SidebarIconedButton {...item}/>)}
      </SidebarItemList>
      <SidebarBottomActions>
        {props.actionItems.map(item =>
          <SidebarIconedButton {...item}/>)}
      </SidebarBottomActions>
      <LogoutButton
        {...props.logoutButtonProps}/>
    </SidebarContainer>
  );
}
