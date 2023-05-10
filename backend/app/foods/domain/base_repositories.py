from app.database.base import Repository
from app.foods.db.portion.model import Portion


class BasePortionsRepository(Repository[Portion]):
    pass
