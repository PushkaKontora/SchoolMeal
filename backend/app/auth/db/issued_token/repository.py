from sqlalchemy import update

from app.auth.db.issued_token.model import IssuedToken
from app.auth.domain.base_repositories import BaseIssuedTokensRepository
from app.database.specifications import FilterSpecification


class IssuedTokensRepository(BaseIssuedTokensRepository):
    async def revoke(self, specification: FilterSpecification) -> None:
        query = specification(update(IssuedToken)).values(revoked=True)

        await self.session.execute(query)
