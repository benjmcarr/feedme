from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    extra_info: str
    quantity: int
    units: str

    def __add__(self, other):
        if self.name != other.name:
            raise ValueError('cannot add different ingredients')
        if self.extra_info != other.extra_info:
            raise ValueError('cannot add different ingredients')
        if self.units != other.units:
            raise ValueError('units mismatch, cannot add')
        return Ingredient(
            name=self.name,
            extra_info=self.extra_info,
            quantity=self.quantity + other.quantity,
            units=self.units
        )

    def __sub__(self, other):
        if self.name != other.name:
            raise ValueError('cannot add different ingredients')
        if self.extra_info != other.extra_info:
            raise ValueError('cannot add different ingredients')
        if self.units != other.units:
            raise ValueError('units mismatch, cannot add')
        if self.quantity - other.quantity < 0:
            raise ValueError('cannot have a negative quantity of an Ingredient')
        return Ingredient(
            name=self.name,
            extra_info=self.extra_info,
            quantity=self.quantity - other.quantity,
            units=self.units
        )
