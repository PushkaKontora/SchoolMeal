import {ControlledInputField} from '../../../controlled-input-field';
import {InputFieldLimitedProps} from '../model/props';
import {createStyle} from '../const/main-styles';
import {View} from 'react-native';
import {SymbolCounter} from '../../symbol-counter';
import {useEffect, useState} from 'react';
import {FormOnChangeText} from '../../../../../model/forms/form-types';
import {applyViewStyle, composeStyles} from '../lib/lib';

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
        data={props.data}
        errors={props.errors}
        style={styles.internalField}
        onChangeText={onChangeText}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        maxLength={props.symbolLimit}
        numberOfLines={props.numberOfLines}
      />
      <SymbolCounter limit={props.symbolLimit} currentSymbols={currentSymbols}/>
    </View>
  );
}
