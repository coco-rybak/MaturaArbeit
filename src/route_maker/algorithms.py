import math
import random
from typing import Final, NamedTuple

DEFAULT_RNG_SEED: Final[int] = 2007

MIN_WALL_HEIGHT: Final[int] = 200
MAX_WALL_HEIGHT: Final[int] = 2000

MIN_WALL_WIDTH: Final[int] = 100
MAX_WALL_WIDTH: Final[int] = 2000

MIN_WEST_ANGLE: Final[int] = 90 + 15
MAX_WEST_ANGLE: Final[int] = 180 - 15
DEFAULT_WEST_ANGLE: Final[int] = 90 + (90 // 2)

MIN_EAST_ANGLE: Final[int] = 0 + 15
MAX_EAST_ANGLE: Final[int] = 90 - 15
DEFAULT_EAST_ANGLE: Final[int] = 90 // 2

MIN_MIN_HOLD_DISTANCE: Final[int] = 20
MAX_MIN_HOLD_DISTANCE: Final[int] = 50
DEFAULT_MIN_HOLD_DISTANCE: Final[int] = 25

MIN_MAX_HOLD_DISTANCE: Final[int] = 50
MAX_MAX_HOLD_DISTANCE: Final[int] = 120
DEFAULT_MAX_HOLD_DISTANCE: Final[int] = 75

DEFAULT_START_DISTANCE: Final[int] = 50
DEFAULT_END_DISTANCE: Final[int] = 50

TYPE_STYLE = {
    0: {"shape": "rect", "w": 10, "h": 3, "fill": "orange"},    # crimp
    1: {"shape": "rect", "w": 15, "h": 15, "fill": "black"},    # jug
    2: {"shape": "circle", "r": 9, "fill": "red"},              # sloper
    3: {"shape": "rect", "w": 4, "h": 15, "fill": "green"},     # pinch
    4: {"shape": "circle", "r": 6, "fill": "yellow"},           # pocket
    5: {"shape": "circle", "r": 2, "fill": "blue"},             # foothold
}

class Hold(NamedTuple):
    x: int
    y: int
    type: int

    def to_svg(self, height) -> str:
        style = TYPE_STYLE.get(self.type, TYPE_STYLE[0])

        # The height parameter is necessary because the SVG standard is 0,0 = top-left. So, just before rendering the hold it's flipped.

        if style["shape"] == "circle":
            return f'<circle cx="{self.x}" cy="{height - self.y}" r="{style["r"]}" fill="{style["fill"]}" />'

        w, h = style["w"], style["h"]
        return f'<rect x="{self.x - w / 2}" y="{height - self.y - h / 2}" width="{w}" height="{h}" fill="{style["fill"]}" />'

def generate_route(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance):
    holds: list[Hold] = []

    # For testing, use an explicit seed value in order to make the run reproducible.
    # rng = random.Random(DEFAULT_RNG_SEED)
    rng = random.Random(None)

    while True:
        if len(holds) == 0:
            holds.append(Hold(
                x = rng.randint(0, width),
                y = rng.randint(0, DEFAULT_START_DISTANCE),
                type = rng.randint(0, 4)))
        else:
            last_hold = holds[-1]

            if height - last_hold.y < DEFAULT_END_DISTANCE:
                break

            while True:
                # TODO: In order to prevent failures we could change the angle allowed when the x coordinate is too close to either side of the wall.

                distance = rng.randint(min_hold_distance, max_hold_distance)
                angle_degrees = rng.randint(east_angle, west_angle)
                angle = math.radians(angle_degrees)

                new_x = last_hold.x + round(distance * math.cos(angle))
                new_y = last_hold.y + round(distance * math.sin(angle))

                if 0 <= new_x <= width:
                    # Insert an occasional foothold, above a certain height. It has to be added before the main hold so it does not affect the
                    # generation of the next 'normal' hold by resetting the height.
                    if new_y > 175 and rng.random() < 0.10:
                        holds.append(Hold(x = new_x, y = new_y - 150, type = 5))
                        print(f"[DEBUG] adding a foothold below: [{new_x}, {new_y}]")

                    holds.append(Hold(x = new_x, y = new_y, type = rng.randint(0, 4)))
                    break
                else:
                    print(f"[DEBUG] failed hold: {distance}+{angle_degrees}:{angle}->[{new_x}, {new_y}]")


    return holds

def generate_svg_preview(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance):
    canvas_w = width
    canvas_h = height

    holds = generate_route(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance)
    print(f"[DEBUG] holds: {holds}")

    svg = f"""<svg viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="max-width:100%; max-height:100%;">
      <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" rx="12" fill="white" stroke="#e5e7eb" stroke-width="2"/>
      <rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" rx="12" fill="#f8fafc" />"""

    for hold in holds:
        svg += hold.to_svg(canvas_h)

    svg += f"""
    <text x="12" y="20" font-family="monospace" font-size="12" fill="#64748b">{canvas_w} x {canvas_h}</text>
    </svg>"""
    return svg