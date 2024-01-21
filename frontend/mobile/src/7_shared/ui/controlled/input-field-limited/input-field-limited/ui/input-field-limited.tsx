import {ControlledInputField} from '../../../controlled-input-field';
import {InputFieldLimitedProps} from '../model/props';
import {createStyle} from '../const/main-styles';
import {View} from 'react-native';
import {SymbolCounter} from '../../symbol-counter';
import {useState} from 'react';
import {FormOnChangeText} from '../../../../../model/forms/form-types';
import {applyViewStyle, composeStyles} from '../lib/lib';
import {DEFAULT_MAX_LENGTH} from '../const/config';

export function InputFieldLimited<FormData>
(props: InputFieldLimitedProps<FormData>) {
  const styles = createStyle(props.style);
  const viewStyles = composeStyles(styles);

  const [currentSymbols, setCurrentSymbols] = useState(0);
  const [focused, setFocused] = useState(false);

  const onChangeText: FormOnChangeText = (text: string) => {
    setCurrentSymbols(text.length);
  };

  return (
    <View
      style={applyViewStyle(viewStyles, focused)}>
      <ControlledInputField
        control={props.control}
        //eslint-disable-next-line
        //@ts-ignore
        data={props.data}
        errors={props.errors}
        style={styles.internalField}
        onChangeText={onChangeText}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        maxLength={props.maxLength || DEFAULT_MAX_LENGTH}
        numberOfLines={props.numberOfLines}
        multiline={true}
        autoFocus={props.autoFocus}
      />
      <SymbolCounter limit={props.maxLength || DEFAULT_MAX_LENGTH} currentSymbols={currentSymbols}/>
    </View>
  );
}
