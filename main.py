from __future__ import annotations
from dataclasses import dataclass, field
from pprint import pprint
# from enum import Enum


@dataclass(repr=False)
class Hold:
    size: str
    type: str
    difficulty: int

    def __repr__(self) -> str:
        return f"This piece is a {self.size} {self.type} and has a difficulty rating of {self.difficulty}."

# class HoldSizes(Hold, Enum):
#     large = "large"
#     medium = "medium"
#     small = "small"
#
# class HoldTypes(Hold, Enum):
#     jug = "jug"
#     crimp = "crimp"
#     foothold = "foothold"
#     pocket = "pocket"
#     sloper = "sloper"
#     pinch = "pinch"

@dataclass(repr=False)
class Route:
    name: str
    holds: list[Hold] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"This Route is named {self.name}. It has {len(self.holds)} holds."


@dataclass(repr=False)
class Wall:
    name: str
    width: int
    height: int
    angle: int
    routes: list[Route] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"This Wall is named {self.name}. It is {self.width} m wide and {self.height} m tall. It is inclined at {self.angle} degrees."


def main() ->None:
    # straight_wall = Wall(length=13, angle=0)
    # five_wall = Wall(length=13, angle=5)
    # ten_wall = Wall(length=13, angle=10)
    # fifteen_wall = Wall(length=13, angle=15)
    #
    # piece1 = Hold(size="large", type="foothold", difficulty=1)
    # piece2 = Hold(size="medium", type="jug", difficulty=10)
    # piece3 = Hold(size="small", type="crimp", difficulty=15)

    route = Route(name="Wädi")
    pprint(route)
    # wall = Wall(name="Uster", width=4, height=13, angle=0)



   # hold1
    #hold2
    #...
    #holdN

    #route1 = Route(name, holds=(hold1, hold2...))
    #route2 ...

    #wall = Wall(name, routes=(route1, route2...))

    #print(wall)

if __name__ == '__main__':
    main()





# @dataclass
# class B:
#     name: str
#     value: float
#
# @dataclass
# class A:
#     label: str
#     # We use field(default_factory=list) to avoid the "mutable default" bug
#     items: list[B] = field(default_factory=list)
#
# # Example Usage:
# item1 = B(name="Widget", value=19.99)
# item2 = B(name="Gadget", value=5.50)
#
# container = A(label="Inventory", items=[item1, item2])
#
# print(container)
# # Output: A(label='Inventory', items=[B(name='Widget', value=19.99), B(name='Gadget', value=5.5)])