import {CalendarProps} from '../model/props';
import {Calendar as ExternalCalendar} from 'react-native-calendars';
import {Text, View} from 'react-native';

export function Calendar(props: CalendarProps) {
  return (
    <ExternalCalendar
      initialDate={'2023-11-01'}
      markingType={'period'}
      hideArrows={true}
      hideExtraDays={true}
      firstDay={1}
      theme={{
        stylesheet: {
          calendar: {

          }
        }
      }}
      markedDates={{
        '2023-11-17': {
          startingDay: true,
          endingDay: false,
          color: '#FFEEE8'
        },
        '2023-11-18': {
          startingDay: false,
          endingDay: false,
          color: '#FFEEE8'
        },
        '2023-11-19': {
          startingDay: false,
          endingDay: true,
          color: '#FFEEE8'
        },
      }}
      dayComponent={(props) => (
        <View style={{
          width: '100%',
          height: 36,
          borderColor: '#aa0000',
          borderWidth: 1,
          alignItems: 'center'
        }}>
          {
            props.marking?.startingDay && (
              <View
                style={{
                  position: 'absolute',
                  left: '50%',
                  width: '50%',
                  height: 36,
                  backgroundColor: '#ffbaa1'
                }}/>
            )
          }
          <View style={{
            width: 36,
            height: 36
          }}>
            <Text style={{
              height: '100%',
              textAlign: 'center',
              verticalAlign: 'middle',
              borderRadius: 50,
              backgroundColor: props.marking?.startingDay ? '#E9632C' : '#00000000'
            }}>
              {props.date?.day}
            </Text>
          </View>
        </View>
      )}
      renderHeader={(date: any) => (
        <Text>
          {'Custom Header'}
        </Text>
      )}
    />
  );
}
