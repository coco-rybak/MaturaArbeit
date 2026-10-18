from pathlib import Path
from typing import Final
import streamlit as st
import json
import xml.etree.ElementTree as ETree

WIDE_CARD_HEIGHT: Final[int] = 300
TALL_CARD_HEIGHT: Final[int] = 500

@st.cache_data
def load_svgs(pattern):
    img_dir = Path(__file__).parent / "images"
    svgs = {}

    for path in sorted(img_dir.glob(pattern)):
        svg_text = path.read_text(encoding="utf-8")

        svg_xml = ETree.fromstring(svg_text)
        metadata_raw = svg_xml.find(f"{{{"http://www.w3.org/2000/svg"}}}metadata")
        metadata_json = {}

        if metadata_raw is not None and metadata_raw.text:
            try:
                metadata_json = json.loads(metadata_raw.text)
            except json.JSONDecodeError:
                metadata_json = {"raw": metadata_raw.text}

        svgs[path.stem] = {
            "id": path.stem,            # filename without .svg
            "metadata": metadata_json,  # geometry values
            "svg": svg_text,            # raw <svg>...</svg>
        }

    return svgs

def generate_cards(svgs, height = WIDE_CARD_HEIGHT):
    bc = "#e5e5e5"
    bw = "1px"
    bg = "white"

    result = f"""
    <style>
    .card-svg {{
      height:{height}px; max-height:{height}px; width:100%;
      display:flex; align-items:center; justify-content:center;
      overflow:hidden;
    }}
    .card-svg svg {{
      height:100% !important;
      max-height:{height}px !important;
      width:100% !important;
      object-fit:contain;
      display:block;
    }}
    </style>
    """

    for svg_id, svg_props in svgs.items():
        result += f"""
        <a href='javascript:void(0)' id='{svg_id}' style="text-decoration:none; display:block; width:100%; margin-bottom:12px; color:inherit;">
          <div style="border:{bw} solid {bc}; border-radius:12px; padding:12px; background:{bg}; cursor:pointer; width:100%; box-sizing:border-box; display:flex;">
            <div class="card-svg">{svg_props['svg']}</div>
          </div>
        </a>
        """

    return result