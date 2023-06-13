import '../consts/style.scss';
import ClassSelectionWidget from "../../../4_widgets/teacher-blocks/class-selection/ui/class-selection.tsx";
import TableWidget from "../../../4_widgets/teacher-blocks/table/ui/table.tsx";

export default function TeacherApplicationPersonal() {

    return (
        <div className="containerTeacherApplication">
            <ClassSelectionWidget/>
            <TableWidget/>
        </div>
    );
}
