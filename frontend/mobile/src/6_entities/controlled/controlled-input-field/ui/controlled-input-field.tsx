import {Controller} from 'react-hook-form';
import {ControlledInputFieldProps} from '../model/props';
import {InputData, InputField} from '../../../../7_shared/ui/fields/input-field';

export function ControlledInputField<FormData>
(props: ControlledInputFieldProps<FormData>) {
  const data: InputData<FormData> = props.data;

  return (
    <Controller
      control={props.control}
      name={data.name}
      rules={data.options}
      render={({field: {onChange, value}}) => (
        <InputField
          data={data}
          value={value}
          onChangeText={onChange}
          style={props.style}
          inputRef={props.inputRef}
          autoFocus={props.autoFocus}
          errors={props.errors}/>
      )}>

    </Controller>
  );
}
