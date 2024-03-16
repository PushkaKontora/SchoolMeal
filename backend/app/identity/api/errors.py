from app.shared.api.errors import APIError


class NotAuthenticated(APIError):
    message = "Пользователь не был аутентифицирован"


class NotRefreshed(APIError):
    message = "Токены не были обновлены. Необходимо пройти повторно аутентификацию"
