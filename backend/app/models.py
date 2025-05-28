from decimal import Decimal
from typing import Union

from pydantic import BaseModel, field_serializer


class Message(BaseModel):
    text: str
    timestamp: str
    report_id: Union[int, None] = None
    id: int

class Report(BaseModel):
    id: int
    name: Union[str, None] = None
    credit_cost: Decimal


class Usage(BaseModel):
    message_id: int
    timestamp: str
    report_name: Union[str, None] = None
    credits_used: Decimal

    # Pydnatic can't serialise Decimal to JSON when we return as API respose
    # So we convert it to float
    @field_serializer('credits_used')
    def serialize_credits_used(self, value: Decimal) -> float:
        return float(value)


class ReportResponse(BaseModel):
    report: Union[Report, None] = None
    status_code: int