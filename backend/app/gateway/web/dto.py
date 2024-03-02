from datetime import date

from pydantic import BaseModel

from app.ipc.nutrition.dto import Override


class SubmitRequestIn(BaseModel):
    on_date: date
    overrides: set[Override]
