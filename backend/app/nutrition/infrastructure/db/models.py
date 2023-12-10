from dataclasses import asdict
from datetime import date
from typing import Any

from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import Mapped

from app.common.infrastructure.db.base import Base
from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriod, CancellationPeriodSequence, SpecifiedReason
from app.nutrition.domain.pupil import FirstName, LastName, Pupil, PupilID


class NutritionSchemaMixin:
    __table_args__ = {"schema": "nutrition"}


class PupilDB(Base, NutritionSchemaMixin):
    __tablename__ = "pupil"

    id: Mapped[str] = Column(String, primary_key=True)
    last_name: Mapped[str] = Column(String, nullable=False)
    first_name: Mapped[str] = Column(String, nullable=False)
    meal_plan: Mapped[dict[str, bool]] = Column(JSON, nullable=False)
    preferential_certificate: Mapped[dict[str, Any] | None] = Column(JSON, nullable=True)
    cancellation_periods: Mapped[list[dict[str, Any]]] = Column(JSON, nullable=False, server_default="[]")

    def to_model(self) -> Pupil:
        return Pupil(
            id=PupilID(self.id),
            last_name=LastName(self.last_name),
            first_name=FirstName(self.first_name),
            meal_plan=MealPlan(**self.meal_plan),
            preferential_certificate=PreferentialCertificate(
                ends_at=date.fromisoformat(self.preferential_certificate["ends_at"])
            )
            if self.preferential_certificate
            else None,
            cancellation_periods=CancellationPeriodSequence(
                periods=tuple(
                    CancellationPeriod(
                        starts_at=date.fromisoformat(period["starts_at"]),
                        ends_at=date.fromisoformat(period["ends_at"]),
                        reasons=frozenset(map(SpecifiedReason, period["reasons"])),
                    )
                    for period in self.cancellation_periods
                )
            ),
        )

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilDB":
        return cls(
            id=pupil.id.value,
            last_name=pupil.last_name.value,
            first_name=pupil.first_name.value,
            meal_plan=asdict(pupil.meal_plan),
            preferential_certificate={
                "ends_at": pupil.preferential_certificate.ends_at.isoformat(),
            }
            if pupil.preferential_certificate
            else None,
            cancellation_periods=[
                {
                    "starts_at": period.starts_at.isoformat(),
                    "ends_at": period.ends_at.isoformat(),
                    "reasons": [reason.value for reason in period.reasons],
                }
                for period in pupil.cancellation_periods
            ],
        )