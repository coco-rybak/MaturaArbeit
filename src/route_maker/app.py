import datetime
import streamlit as st
from collections import namedtuple
from st_click_detector import click_detector
from resources import load_svgs, generate_cards, WIDE_CARD_HEIGHT, TALL_CARD_HEIGHT
from algorithms import generate_svg_preview
import algorithms as ALGO_LIMITS

st.set_page_config(layout="centered")
st.title("Climbing Route Maker")

# We use a 'wizard'-like interface here which is not a native concept in Streamlit. It's something that can be accomplished by using session_state
# variables which then manage which bits of the UI are turned on and off in turn. Streamlit runs all the code over an over on user input so normal
# variables always get reset but session_state is magical and persists for the duration of the app's execution.
#
# It's always possible to log to the console a variable you're interested in with code like this:
#
# print(f"[DEBUG] clicked: {clicked}")
#
# However, this snippet here below add the contents of the session_state to the (expandable) sidebar.
@st.fragment
def debug_sidebar():
    with st.sidebar:
        st.subheader("Session State")
        st.json(dict(st.session_state), expanded=False)
        if st.button("Clear state"):
            st.session_state.clear()
            st.rerun()

debug_sidebar()

def generate_custom_filename():
    start = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    uniqueness = int((now - start).total_seconds() * 1000)
    return f"route_{st.session_state.get("2", 0)}x{st.session_state.get("1", 0)}_{uniqueness}.svg"


# Disable the wall selection.
#
# if 'selected_wall' not in st.session_state:
#     st.divider()
#     st.markdown("""**Please select a wall:**""")
#
#     # The routing algorithms need some properties of the wall. Since we already have svg files to represent the walls, I am going to use them to
#     # store the extra data. At the moment that extra data is just default width and height but in a real application you could have a lot more
#     # geometry data to describe the real wall. Then the more appropriate place would be a database or perhaps just JSON files.
#     #
#     # So what is going on here is the svg files are loaded and the 'metadata' is read in together with the svg visual data. Then, when the
#     # click_detector returns the id of the selected wall, that id is used to look up the metadata. The metadata is then added to the session state to
#     # be used by whatever algorithm runs.
#     svgs = load_svgs("wall_*.svg")
#     clicked = click_detector(generate_cards(svgs, WIDE_CARD_HEIGHT))
#
#     if clicked:
#         st.session_state.selected_wall = clicked
#         st.session_state.wall_metadata = svgs[clicked]["metadata"]
#
#         # Here we force a manual rerun of the logic which gets us in the next page of the wizard.
#         st.rerun()
#
# elif 'selected_algo' not in st.session_state:
if 'selected_algo' not in st.session_state:
    st.divider()
    st.markdown("""**Please select a routing algorithm:**""")

    # There are no extra bits of metadata stored in the algo svgs. There could be but for the moment it is the code that contains any defaults.
    # Still, we use the same logic pattern just in case we change our minds later.
    svgs = load_svgs("algo_*.svg")
    clicked = click_detector(generate_cards(svgs, TALL_CARD_HEIGHT))

    if clicked:
        st.session_state.selected_algo = clicked

        if 'wall_metadata' not in st.session_state:
            st.session_state.wall_metadata = {"width": "300", "height": "500"}

        st.rerun()

else:
    st.divider()

    # There is only one algorithm at the moment so this next bit of code is not needed. But in principle this is one way to dynamically find the
    # right algorithm implementation just based on the name of the file the user picked in the previous step. Once you have the 'index' then you
    # pull up the right algorithm in a list of algorithms and use the 'description' in the UI as a title, etc.
    filename_parts = st.session_state.selected_algo.split('_', 2)
    algo_entry = namedtuple('algo_entry', ['prefix', 'index', 'description'])
    parsed_algo_entry = algo_entry(filename_parts[0], int(filename_parts[1]), filename_parts[2].replace('_', ' ').capitalize().rstrip('.') + '.')
    print(f"[DEBUG] parsed_algo_entry: {parsed_algo_entry}")

    with st.form("algo_properties"):
        header = st.columns([1])
        header[0].subheader('Algorithmus I')


        header = st.columns([1])
        header[0].subheader('Properties / Eigenschaften')

        row1 = st.columns([1])
        default_height = int(st.session_state.wall_metadata["height"])
        height = row1[0].slider('Height / Höhe', ALGO_LIMITS.MIN_WALL_HEIGHT, ALGO_LIMITS.MAX_WALL_HEIGHT, default_height, step=25, key=1)

        row2 = st.columns([1])
        default_width = int(st.session_state.wall_metadata["width"])
        width = row2[0].slider('Width / Breite', ALGO_LIMITS.MIN_WALL_WIDTH, ALGO_LIMITS.MAX_WALL_WIDTH, default_width, step=25, key=2)

        row3 = st.columns([1])
        default_west_angle = ALGO_LIMITS.DEFAULT_WEST_ANGLE
        west_angle = row3[0].slider('Left Angle / linker Winkel', ALGO_LIMITS.MIN_WEST_ANGLE, ALGO_LIMITS.MAX_WEST_ANGLE, default_west_angle, step=5, key=3)

        row4 = st.columns([1])
        default_east_angle = ALGO_LIMITS.DEFAULT_EAST_ANGLE
        east_angle = row4[0].slider('Right Angle / rechter Winkel', ALGO_LIMITS.MIN_EAST_ANGLE, ALGO_LIMITS.MAX_EAST_ANGLE, default_east_angle, step=5, key=4)

        row5 = st.columns([1])
        default_min_hold_distance = ALGO_LIMITS.DEFAULT_MIN_HOLD_DISTANCE
        min_hold_distance = row5[0].slider('Min Hold Distance / Mindestabstand', ALGO_LIMITS.MIN_MIN_HOLD_DISTANCE, ALGO_LIMITS.MAX_MIN_HOLD_DISTANCE, default_min_hold_distance, step=5, key=5)

        row6 = st.columns([1])
        default_max_hold_distance = ALGO_LIMITS.DEFAULT_MAX_HOLD_DISTANCE
        max_hold_distance = row6[0].slider('Max Hold Distance / Maximalabstand', ALGO_LIMITS.MIN_MAX_HOLD_DISTANCE, ALGO_LIMITS.MAX_MAX_HOLD_DISTANCE, default_max_hold_distance, step=5, key=6)

        st.divider()
        submitted = st.form_submit_button('Generate Route / Route generieren', use_container_width=True, type="primary")

    if submitted:
        svg_code = generate_svg_preview(height, width, west_angle, east_angle, min_hold_distance, max_hold_distance)

        html = f"""
        <div style="width:100%; height:500px; border:1px solid #e5e7eb; border-radius:12px; background:white; display:flex; align-items:center; justify-content:center; padding:16px; overflow:hidden; box-sizing:border-box;">
            {svg_code}
        </div>
        """

        with st.container(border=True):
            header = st.columns([1])
            header[0].subheader('Output')

            st.iframe(html, height=532)
            st.download_button(
                "Download SVG / SVG-Datei herunterladen",
                data=svg_code,
                file_name=generate_custom_filename(),
                mime="image/svg+xml",
                width='stretch')