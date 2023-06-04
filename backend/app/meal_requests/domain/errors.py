from app.utils.error import Error


class NotFoundCreatorError(Error):
    @property
    def message(self) -> str:
        return "Not found creator by id"


class MealRequestAlreadyExistsError(Error):
    @property
    def message(self) -> str:
        return "Request is already sent on meal"


class MealDoesNotExistError(Error):
    @property
    def message(self) -> str:
        return "Meal does not exists"


class InvalidPupilsSequenceError(Error):
    @property
    def message(self) -> str:
        return "Pupil ids in body do not match with pupils in the school class"


class NotFoundMealRequestError(Error):
    @property
    def message(self) -> str:
        return "Not found meal request with the id"


class UpdatingFrozenRequestError(Error):
    @property
    def message(self) -> str:
        return "The request cannot be changed after time expiration"
