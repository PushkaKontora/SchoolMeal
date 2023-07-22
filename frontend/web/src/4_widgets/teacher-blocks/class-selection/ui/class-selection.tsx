import '../consts/style.scss';
import {ClassSelectionProps} from "../model/props.ts";
import ClassItemWidget from "../../class-item/ui/class-item.tsx";
import leftArrow from "../../../../7_shared/assets/images/leftArrow.jpg";
import rightArrow from "../../../../7_shared/assets/images/rightArrow.jpg";

export default function ClassSelectionWidget(props: ClassSelectionProps) {

    const classArray = ['3А', '3Б', '3В', '3Г'];

    return (
        <div className="containerClassSelection">
            <div className="headerTable">
                <div className='containerClassItems'>
                    {classArray.map((item) => (
                        <ClassItemWidget key={item}
                                         className={item}/>
                    ))}
                </div>
                <div className="date">
                    <img src={leftArrow} alt='this is top image'/>
                    <div className="text">среда 15.05</div>
                    <img src={rightArrow} alt='this is top image'/>
                </div>
            </div>
        </div>
    );
}

