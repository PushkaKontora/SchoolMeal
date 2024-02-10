import {ControlledInputFieldProps} from './props.ts';
import {Controller} from 'react-hook-form';
import {InputField} from '../input-field';

export function ControlledInputField<FormData>(props: ControlledInputFieldProps<FormData>) {
  const data = props.data;

  return (
    <Controller
      control={props.control}
      name={data.name}
      rules={data.options}
      render={({field: {onChange, value}}) => (
        <InputField
          style={props.style}
          data={data}
          value={value}
          onChangeText={onChange}
          errors={props.errors}/>
      )}/>
  );
}
