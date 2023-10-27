import '../consts/style.scss';
import {CHILDRENS_NAME} from '../../../../3_pages/teacher-main-page/consts/moks.ts';

export default function TableWidget() {

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
          {CHILDRENS_NAME.map((item) => (
            <tr className='tr' key={item.id}>
              <td scope="row">
                <input type="checkbox"
                  className="custom-checkbox custom-checkbox__firstCol"
                  id={item.id}
                  name={item.id}
                  value="yes"/>
                <label htmlFor={item.id}>
                  <div className='checkChild checkChild__name'>{item.price}₽</div>
                  <div className='nameChild'>{item.name}</div>
                </label>
              </td>
            </tr>
          ))}
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
          {CHILDRENS_NAME.map((item) => (
            <tr className='tr' key={item.id + 100}>
              <td scope="row">
                <input type="checkbox"
                  className="custom-checkbox"
                  id={item.id + 100}
                  name={item.id + 100}
                  value="yes"/>
                <label htmlFor={item.id + 100}/>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <table className='table table__t3'>
        <thead>
          <tr>
            <td scope="col">
              <div className="nameCol">Обед</div>
              <div className="price">147₽</div>
            </td>
          </tr>
        </thead>
        <tbody>
          {CHILDRENS_NAME.map((item) => (
            <tr className='tr' key={item.id + 200}>
              <td scope="row">
                <input type="checkbox"
                  className="custom-checkbox"
                  id={item.id + 200}
                  name={item.id + 200}
                  value="yes"/>
                <label htmlFor={item.id + 200}/>
              </td>
            </tr>
          ))}
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
          {CHILDRENS_NAME.map((item) => (
            <tr className='tr' key={item.id + 300}>
              <td scope="row">
                <input type="checkbox"
                  className="custom-checkbox"
                  id={item.id + 300}
                  name={item.id + 300}
                  value="yes"/>
                <label htmlFor={item.id + 300}/>
              </td>
            </tr>
          ))}
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
          {CHILDRENS_NAME.map((item) => (
            <tr className='tr' key={item.id + 400}>
              <td scope="row">
                <div className='checkChild'>{item.total}₽</div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

