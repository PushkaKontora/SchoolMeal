import {Content, ParentContainer} from './styles.ts';
import {SidebarWithContentProps} from './props.ts';
import {SIDEBAR_WIDTH} from '../../config/config.ts';
import {PaddingArea} from '../../../markup/padding-area';

export function SidebarWithContent(props: SidebarWithContentProps) {
  return (
    <ParentContainer
      $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
      {props.sidebar}
      <Content
        $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
        <PaddingArea
          padding={props.contentStyles?.padding}>
          {props.children}
        </PaddingArea>
      </Content>
    </ParentContainer>
  );
}
