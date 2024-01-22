import {ClassSelectorProps} from './props.ts';
import {ButtonSecondary} from '../../buttons/button-secondary';
import {Tabs} from '../../../../4_widgets/meal-application-widget/ui/styles.ts';
import {useState} from 'react';

export function ClassSelector(props: ClassSelectorProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  return (
    <Tabs>
      {
        props.config.map((item, idx) => (
          <ButtonSecondary
            title={item.name}
            backgroundColor={selectedIndex !== idx ? '#F3F6F9' : undefined}
            textColor={selectedIndex !== idx ? '#B4B4B4' : undefined}
            onPress={() => {
              item.onClick(idx);
              setSelectedIndex(idx);
            }
          }/>
        ))
      }
    </Tabs>
  );
}
