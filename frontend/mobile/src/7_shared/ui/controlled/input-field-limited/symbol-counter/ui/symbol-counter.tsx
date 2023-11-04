import {Text, View} from 'react-native';
import {createStyle} from '../const/symbol-counter-styles';
import {useEffect, useState} from 'react';
import {SymbolCounterProps} from '../model/props';
import {createString} from '../lib/lib';

export function SymbolCounter(props: SymbolCounterProps) {
  const [text, setText] = useState(createString(props));

  useEffect(() => {
    setText(createString(props));
  }, [props.currentSymbols, props.limit]);

  const styles = createStyle();

  return (
    <View>
      <Text
        style={styles.symbolCounter}>
        {text}
      </Text>
    </View>
  );
}
