import TeacherApplyApplicationWidget
    from "../../../4_widgets/teacher-apply-application/ui/teacher-apply-application.tsx";
import HeaderTeacherWidget from "../../../4_widgets/header-teacher/ui/header-teacher.tsx";
import '../consts/style.scss'

export function TeacherMainPage() {
    return (
        <div className='containerTeacherMain'>
            <HeaderTeacherWidget/>
            <TeacherApplyApplicationWidget statusName={'Не подана'}/>
        </div>
    );
}
