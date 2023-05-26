export function setCheckAt(index: number, itemNumber: number) {
  const nextState = Array(itemNumber).fill(false);
  nextState[index] = true;
  return nextState;
}
