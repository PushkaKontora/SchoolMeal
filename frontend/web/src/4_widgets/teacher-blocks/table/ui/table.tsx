import '../consts/style.scss';
import {TableProps} from "../model/props.ts";

export default function TableWidget(props: TableProps) {

    return (
        <div className="containerTable">
            <table className='table table__t1'>
                <thead>
                <tr>
                    <td scope="col">
                        <input type="checkbox"
                               className="custom-checkbox custom-checkbox__firstCol"
                               id="name"
                               name="name"
                               value="yes"/>
                        <label htmlFor="name">ФИО</label>
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr className='tr'>
                    <td scope="row">
                        <input type="checkbox"
                               className="custom-checkbox custom-checkbox__firstCol"
                               id="1"
                               name="1"
                               value="yes"/>
                        <label htmlFor="1">
                            <div className='checkChild checkChild__name'>1222₽</div>
                            <div className='nameChild'>Ковешникова Татьяна Анатольевна</div>
                        </label>
                    </td>
                </tr>
                </tbody>
            </table>
            <table className='table table__t2'>
                <thead>
                <tr>
                    <td scope="col">
                        <div className="nameCol">Завтрак</div>
                        <div className="price">81₽</div>
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr className='tr'>
                    <td scope="row">
                        <input type="checkbox"
                               className="custom-checkbox"
                               id="2"
                               name="2"
                               value="yes"/>
                        <label htmlFor="2"/>
                    </td>
                </tr>
                </tbody>
            </table>
            <table className='table table__t3'>
                <thead>
                <tr>
                    <td scope="col">
                        <div className="nameCol">Обед</div>
                        <div className="price">121₽</div>
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr className='tr'>
                    <td scope="row">
                        <input type="checkbox"
                               className="custom-checkbox"
                               id="3"
                               name="3"
                               value="yes"/>
                        <label htmlFor="3"/>
                    </td>
                </tr>
                </tbody>
            </table>
            <table className='table table__t4'>
                <thead>
                <tr>
                    <td scope="col">
                        <div className="nameCol">Полдник</div>
                        <div className="price">80₽</div>
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr className='tr'>
                    <td scope="row">
                        <input type="checkbox"
                               className="custom-checkbox"
                               id="5"
                               name="5"
                               value="yes"/>
                        <label htmlFor="5"/>
                    </td>
                </tr>
                </tbody>
            </table>
            <table className='table table__t5'>
                <thead>
                <tr>
                    <td scope="col">
                        <div className="nameCol">Итого</div>
                    </td>
                </tr>
                </thead>
                <tbody>
                <tr className='tr'>
                    <td scope="row">
                        <div className='checkChild'>121₽</div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    );
}

