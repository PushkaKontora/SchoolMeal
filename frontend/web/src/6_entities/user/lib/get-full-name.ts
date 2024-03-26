export function getFullName(userName: {
  firstName?: string,
  lastName?: string
}) {
  return `${userName.firstName || ''} ${userName.lastName || ''}`;
}
