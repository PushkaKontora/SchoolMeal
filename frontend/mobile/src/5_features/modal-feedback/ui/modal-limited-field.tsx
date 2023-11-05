import {ModalLimitedFieldProps} from '../model/props';
import {createStyle} from '../const/limited-field-styles';
import {View} from 'react-native';
import {InputFieldLimited} from '../../../7_shared/ui/controlled/input-field-limited';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {useForm} from 'react-hook-form';
import {INPUT_DATA} from '../const/input-data';
import {LimitedFieldData} from '../types/limited-field-data';
import {DEFAULT_NUMBER_OF_LINES} from '../const/config';

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
        maxLength={props.symbolLimit}
        numberOfLines={DEFAULT_NUMBER_OF_LINES}
        control={control}
        data={INPUT_DATA[0]}
        errors={errors}
      />
      <ButtonPrimary
        title={props.buttonTitle}
        fontSize={12}
        fontWeight={'700'}
        paddingVertical={12}
        backgroundColor={'#EC662A'}
        onPress={handleSubmit(props.onSubmit)}/>
    </View>
  )
}
