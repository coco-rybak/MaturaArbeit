import argparse
import json
import sys
from pathlib import Path

import drawsvg as draw
from jsonschema import ValidationError, validate


class ClimbingTopo:
    def __init__(self, width=500, height=800):
        self.d = draw.Drawing(width, height)
        # Background: light gray wall
        self.d.append(draw.Rectangle(0, 0, width, height, fill="#f0f0f0"))

    def draw_hold(self, hold):
        x, y = hold["x"], hold["y"]
        h_type = hold.get("type", "default")

        # Define styles for different hold types
        if h_type == "jug":
            self.d.append(draw.Circle(x, y, 12, fill="#8B4513", stroke="black"))  # Large brown
        elif h_type == "crimp":
            self.d.append(draw.Rectangle(x - 10, y - 3, 20, 6, fill="#333", rx=2))  # Thin black
        elif h_type == "sloper":
            self.d.append(draw.Circle(x, y, 18, fill="#55acee", fill_opacity=0.6))  # Blue blob
        else:
            # Default "dot"
            self.d.append(draw.Circle(x, y, 6, fill="red", stroke="black"))

    def render(self, data):
        hold_lookup = {h["id"]: h for h in data["holds"]}

        # 1. Draw the route line (dashed path)
        points = []
        for hold_id in data["route"]:
            if hold_id in hold_lookup:
                h = hold_lookup[hold_id]
                points.extend([h["x"], h["y"]])

        if len(points) >= 4:
            self.d.append(draw.Lines(*points, close=False, fill="none", stroke="#999", stroke_width=3, stroke_dasharray="10,5"))

        # 2. Draw the holds on top
        for h in data["holds"]:
            self.draw_hold(h)


def main():
    # Set up Command Line Arguments
    parser = argparse.ArgumentParser(description="Generate a climbing route SVG from JSON.")
    parser.add_argument("input", help="Path to the route JSON file")
    parser.add_argument("--schema", default="climbing-schema.json", help="Path to the JSON schema file")

    args = parser.parse_args()
    input_path = Path(args.input)
    schema_path = Path(args.schema)

    # 1. Load Files
    try:
        with open(input_path, "r") as f:
            route_data = json.load(f)
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {input_path} is not a valid JSON file.")
        sys.exit(1)

    # 2. Validate against Schema
    try:
        validate(instance=route_data, schema=schema)
        print(f"✓ {input_path.name} is valid.")
    except ValidationError as e:
        print(f"❌ Validation Error in {input_path.name}:")
        print(f"  Field: {'.'.join(str(v) for v in e.path)}")
        print(f"  Message: {e.message}")
        sys.exit(1)

    # 3. Generate SVG
    output_filename = input_path.with_suffix(".svg")
    topo = ClimbingTopo()
    topo.render(route_data)

    topo.d.save_svg(str(output_filename))
    print(f"🚀 SVG generated successfully: {output_filename}")


if __name__ == "__main__":
    main()
