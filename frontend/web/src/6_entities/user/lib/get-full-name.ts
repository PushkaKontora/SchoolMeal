export function getFullName(userName: {
  firstName?: string,
  lastName?: string,
  patronymic?: string
}) {
  return `${userName.firstName || ''} ${userName.lastName || ''} ${userName.patronymic || ''}`;
}
