import {ChildInformationProps} from "../model/props";
import {
    ChildPersonalInformation
} from "../../../4_widgets/child/child-information/child-personal-information/ui/child-personal-information";

export function ChildInformationPage(props: ChildInformationProps) {

    return (
        <>
            <ChildPersonalInformation childInformation={props.childInformation}/>
        </>
    );
}
