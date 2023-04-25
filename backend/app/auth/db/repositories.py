from sqlalchemy import select, update

from app.auth.db.models import IssuedToken, Password
from app.auth.domain.base_repositories import BaseIssuedTokensRepository, BasePasswordsRepository
from app.database.specifications import FilterSpecification


class PasswordsRepository(BasePasswordsRepository):
    async def get_last(self, specification: FilterSpecification) -> Password | None:
        query = specification(select(Password).order_by(Password.created_at.desc()).limit(1))

        return await self.session.scalar(query)


class IssuedTokensRepository(BaseIssuedTokensRepository):
    async def revoke(self, specification: FilterSpecification) -> None:
        query = specification(update(IssuedToken)).values(revoked=True)

        await self.session.execute(query)
