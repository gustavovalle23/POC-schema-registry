from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from domain.errors import EntityValidationException
from domain.validators import FoodValidatorFactory


@dataclass(frozen=True)
class Product:
    name: str
    id: Optional[int] = None
    quantity: Optional[int] = 1
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=datetime.now)

    def __post__init__(self):
        if not self.created_at:
            self._set("created_at", datetime.now())
        self.validate()

    def increment_quantity(self, quantity: int) -> int:
        if quantity > 0:
            self._set("quantity", self.quantity + quantity)
        return self.quantity

    def validate(self):
        validator = FoodValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())

        if not is_valid:
            raise EntityValidationException(validator.errors)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "quantity": self.quantity}
