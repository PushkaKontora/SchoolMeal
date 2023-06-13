import '../consts/style.scss';
import {TableProps} from "../model/props.ts";

export default function TableWidget(props: TableProps) {

    return (
        <div className="containerTable">
            <table className='table'>
                <thead>
                <tr>
                    <th scope="col">
                        <input type="checkbox" className="custom-checkbox" id="happy" name="happy" value="yes"/>
                        <label htmlFor="happy">ФИО</label>
                    </th>
                    <th scope="col">
                        <div className="nameCol">Завтрак</div>
                        <div className="price">81₽</div>
                    </th>
                    <th scope="col">
                        <div className="nameCol">Обед</div>
                        <div className="price">147₽</div>
                    </th>
                    <th scope="col">
                        <div className="nameCol">Полдник</div>
                        <div className="price">80₽</div>
                    </th>
                    <th scope="col">
                        <div className="nameCol">Итого</div>
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <th scope="row">Buzzcocks</th>
                    <td>1976</td>
                    <td>9</td>
                    <td>Ever fallen in love (with someone you shouldn't've)</td>
                </tr>
                <tr>
                    <th scope="row">The Clash</th>
                    <td>1976</td>
                    <td>6</td>
                    <td>London Calling</td>
                </tr>
                </tbody>
            </table>

        </div>
    );
}

