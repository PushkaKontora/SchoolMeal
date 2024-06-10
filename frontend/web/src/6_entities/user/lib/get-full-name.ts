export function getFullName(userName: {
  firstName?: string,
  lastName?: string,
  patronymic?: string
}) {
  return `${userName.lastName || ''} ${userName.firstName || ''} ${userName.patronymic || ''}`;
}
