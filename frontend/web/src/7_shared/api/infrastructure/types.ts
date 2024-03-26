export type ApiWithUseFunction<K> = {
  use: (version: K) => any
}
