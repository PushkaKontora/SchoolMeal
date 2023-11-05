import {Controller} from 'react-hook-form';
import {ControlledInputFieldProps} from '../model/props';
import {InputData, InputField} from '../../../fields/input-field';

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
          onChangeText={(text: string) => {
            onChange();
            props?.onChangeText?.(text);
          }}
          onFocus={props.onFocus}
          onBlur={props.onBlur}
          style={props.style}
          maxLength={props.maxLength}
          numberOfLines={props.numberOfLines}
          multiline={props.multiline}
          inputRef={props.inputRef}
          autoFocus={props.autoFocus}
          errors={props.errors}/>
      )}>

    </Controller>
  );
}
