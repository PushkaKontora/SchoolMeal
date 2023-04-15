from sqlalchemy import select, update

from app.auth.db.repositories import IIssuedTokensRepository, IPasswordsRepository
from app.auth.db.sqlalchemy.models import IssuedToken as IssuedTokenModel, Password as PasswordModel
from app.auth.domain.entities import Password
from app.database.specifications import FilterSpecification
from app.database.sqlalchemy.base import AlchemyRepository


class AlchemyPasswordsRepository(IPasswordsRepository, AlchemyRepository):
    async def get_last(self, specification: FilterSpecification) -> Password | None:
        query = specification.to_query(select(PasswordModel).order_by(PasswordModel.created_at.desc()).limit(1))
        password = await self.session.scalar(query)

        return Password.from_orm(password) if password else None


class AlchemyIssuedTokensRepository(IIssuedTokensRepository, AlchemyRepository):
    def create(self, user_id: int, token: str) -> None:
        self.session.add(IssuedTokenModel(user_id=user_id, value=token))

    async def revoke(self, specification: FilterSpecification) -> None:
        query = specification.to_query(update(IssuedTokenModel)).values(revoked=True)

        await self.session.execute(query)
