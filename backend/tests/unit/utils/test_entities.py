import pytest

from app.utils.entities import BaseEntity


class Entity(BaseEntity):
    one: int
    one_two: int
    one_two_three: int


@pytest.fixture(scope="module")
def entity(one=1, one_two=2, one_two_three=3) -> Entity:
    return Entity(one=one, one_two=one_two, one_two_three=one_two_three)


@pytest.mark.unit
def test_camelize_alias_of_entity_fields(entity: Entity):
    expected = {"one": entity.one, "oneTwo": entity.one_two, "oneTwoThree": entity.one_two_three}

    assert entity.dict(by_alias=True) == expected


@pytest.mark.unit
def test_immutability_of_entity(entity: Entity):
    with pytest.raises(Exception):
        entity.one = 10
