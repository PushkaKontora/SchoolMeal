import {Content, ContentBody, ParentContainer} from './styles.ts';
import {SidebarWithContentProps} from './props.ts';
import {SIDEBAR_WIDTH} from '../config/config.ts';

export function SidebarWithContent(props: SidebarWithContentProps) {
  return (
    <ParentContainer
      $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
      {props.sidebar}
      <Content
        $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
        <ContentBody
          $padding={props.contentStyles?.padding}>
          {props.children}
        </ContentBody>
      </Content>
    </ParentContainer>
  );
}
