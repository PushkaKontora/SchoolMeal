from sqlalchemy import select

from app.auth.db.password.model import Password
from app.auth.domain.base_repositories import BasePasswordsRepository
from app.database.specifications import FilterSpecification


class PasswordsRepository(BasePasswordsRepository):
    async def get_last(self, specification: FilterSpecification) -> Password | None:
        query = specification(select(Password).order_by(Password.created_at.desc()).limit(1))

        return await self.session.scalar(query)
