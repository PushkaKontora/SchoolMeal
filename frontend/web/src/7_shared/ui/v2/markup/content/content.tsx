import {ContentProps} from './props';
import {Container} from './styles';

export function Content(props: ContentProps) {
  const {children, ...otherProps} = props;

  return (
    <Container
      {...otherProps}>
      {children}
    </Container>
  );
}
