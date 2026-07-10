import argparse
import json
import sys
from pathlib import Path

import drawsvg as draw

# TODOs
#
# - The coordinates are set up so that the top right corner is at (0,0). Which may not be intuitive since you start climbing from the bottom?
# - All the holds are rendered, even if they do not belong to any route.
# - Perhaps it makes sense to add the wall width and height to the json rather than assuming it here.


class WallRenderer:
    def __init__(self, width=500, height=800):
        self.d = draw.Drawing(width, height)
        self.d.append(draw.Rectangle(0, 0, width, height, fill="#f0f0f0"))

    def draw_hold(self, hold):
        x, y = hold["x"], hold["y"]

        self.d.append(draw.Circle(x, y, 6, fill="red", stroke="black"))

    def render(self, data):
        hold_lookup = {h["id"]: h for h in data["holds"]}

        points = []
        for hold_id in data["route"]:
            if hold_id in hold_lookup:
                h = hold_lookup[hold_id]
                points.extend([h["x"], h["y"]])

        if len(points) >= 4:
            self.d.append(draw.Lines(*points, close=False, fill="none", stroke="#999", stroke_width=3, stroke_dasharray="10,5"))

        for h in data["holds"]:
            self.draw_hold(h)


def main():
    parser = argparse.ArgumentParser(description="Render a climbing route from JSON as an SVG.")
    parser.add_argument("input", help="Path to the JSON route file.")

    args = parser.parse_args()
    input_path = Path(args.input)

    try:
        with open(input_path, "r") as f:
            route_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {input_path} is not a valid JSON file.")
        sys.exit(1)

    output_filename = input_path.with_suffix(".svg")
    renderer = WallRenderer()
    renderer.render(route_data)

    renderer.d.save_svg(str(output_filename))
    print(f"SVG output: {output_filename}")


if __name__ == "__main__":
    main()
