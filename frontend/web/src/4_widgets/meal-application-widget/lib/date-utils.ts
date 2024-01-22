export function dateToISOString(d: Date) {
  return d.toISOString().slice(0,10);
}
