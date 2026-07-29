from pydantic import BaseModel, Field, PositiveFloat
from typing import Optional

class CostCreateSchema(BaseModel):
    description : str = Field(
        ...,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9\s\u0600-\u06FF\.\-\_]+$",
        title='Cost Description'
    )

    amount : PositiveFloat

class CostUpdateSchema(BaseModel):
    description : Optional[str] = Field(
        None,
        min_length=3,
        max_length=100, 
        pattern=r"^[a-zA-Z0-9\s\u0600-\u06FF\.\-\_]+$"
    )

    amount : Optional[PositiveFloat] = None