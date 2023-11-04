import {ModalLimitedFieldProps} from '../model/props';
import {createStyle} from '../const/styles';
import {View} from 'react-native';
import {InputFieldLimited} from '../../../7_shared/ui/controlled/input-field-limited';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {useForm} from 'react-hook-form';
import {INPUT_DATA} from '../const/input-data';
import {LimitedFieldData} from '../types/limited-field-data';

export function ModalLimitedField(props: ModalLimitedFieldProps) {
  const {
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<LimitedFieldData>({
    mode: 'onChange'
  });

  const styles = createStyle();

  return (
    <View
      style={styles.container}>
      <InputFieldLimited 
        symbolLimit={props.symbolLimit}
        control={control}
        data={INPUT_DATA[0]}
        errors={errors}
      />
      <ButtonPrimary
        title={props.buttonTitle}
        onPress={handleSubmit(props.onSubmit)}/>
    </View>
  )
}
