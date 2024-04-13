export function transformDateForReason(date: Date) {
  return date.toLocaleString('ru-RU', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit'
  });
}
