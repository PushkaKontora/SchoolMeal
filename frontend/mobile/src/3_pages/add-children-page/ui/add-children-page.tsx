import {AddChildrenWidget} from '../../../4_widgets/add-children/ui/add-children';
import {AddChildrenPageProps} from "../model/props";

export function AddChildrenPage({navigation}: AddChildrenPageProps) {
  return (
    <AddChildrenWidget navigation={navigation}/>
  );
}
