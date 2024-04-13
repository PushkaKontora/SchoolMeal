export type MealtimeOut =
  'breakfast'
  | 'dinner'
  | 'snacks';

export type MealtimesPatchBody = {
  mealtimes: {
    [key in MealtimeOut]?: boolean
  }
}
