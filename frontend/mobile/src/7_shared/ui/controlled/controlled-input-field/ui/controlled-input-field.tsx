import {Controller} from 'react-hook-form';
import {ControlledInputFieldProps} from '../model/props';
import {InputData, InputField} from '../../../fields/input-field';

export function ControlledInputField<FormData extends {[key: string]: any}>
(props: ControlledInputFieldProps<FormData>) {
  const data: InputData<FormData> = props.data;

  return (
    <Controller
      control={props.control}
      //eslint-disable-next-line
      //@ts-ignore
      name={data.name}
      rules={data.options}
      render={({field: {onChange, value}}) => (
        <InputField
          data={data}
          value={value}
          onChangeText={(text: string) => {
            onChange(text);
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
