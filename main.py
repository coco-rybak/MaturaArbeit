from dataclasses import dataclass
from enum import Enum



@dataclass(repr=False)
class Wall:
    length: int
    angle: int

    def __repr__(self) -> str:
        return f"This Wall is {self.length} m long and has a {self.angle} inclination."

straight_wall = Wall(length=13, angle=0)
five_wall= Wall(length=13, angle=5)
ten_wall = Wall(length=13, angle=10)
fifteen_wall = Wall(length=13, angle=15)



@dataclass(repr=False)
class Hold:
    size: str
    type: str
    difficulty: int

class HoldSizes(Hold, Enum):
    large = "large"
    medium = "medium"
    small = "small"

class HoldTypes(Hold, Enum):
    jug = "jug"
    crimp = "crimp"
    foothold = "foothold"
    pocket = "pocket"
    sloper = "sloper"
    pinch = "pinch"

    def __repr__(self) -> str:
     return f"This piece is a {self.size} {self.type} and has a difficulty rating of {self.difficulty}."

piece1 = Hold(size="large", type="foothold", difficulty=1)
piece2 = Hold(size= "medium", type= "jug", difficulty= 10)
piece3 = Hold(size="small", type= "crimp", difficulty= 15)

@dataclass(repr=False)
class Route:



if __name__ == '__main__':
        print(piece1)

# Bewertung für Schwierigkeiten:
# 3-4c: 0 - 0.2
# 5a-5c : 0.2 - 0.3
# 6a-6a+ : 0.3 - 0.4
# 6b-6b+ : 0.4 - 0.5
# 6c-6c+ : 0.5 - 0.6
# 7a-7a+ : 0.6 - 0.7
# 7b-7b+ : 0.7 - 0.8
# 7c-7c+ : 0.8 - 0.9
# 8a-9a : 0.9 - 1

#Beispiel: 6b-6b+ Route, mit grossen Griffen, Wand bei 90°:
#Wand: 0
#Griffe: 0.1
#Abstand: 0.25
#Neigung: 0.1






