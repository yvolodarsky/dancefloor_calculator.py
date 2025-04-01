import streamlit as st
import numpy as np
import math

st.title("🪩 LED Dance Floor Designer – Panel Grid")

# Inputs for dance floor dimensions
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20)
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20)

# Constants: Panel size (20 inches converted to feet) and cost per square foot
panel_size_ft = 20 / 12
cost_per_sqft = 15

# Calculate grid dimensions based on panel size
cols = math.ceil(width_ft / panel_size_ft)
rows = math.ceil(length_ft / panel_size_ft)
total_panels = cols * rows

actual_width = cols * panel_size_ft
actual_length = rows * panel_size_ft
total_sqft = actual_width * actual_length
total_cost = total_sqft * cost_per_sqft

st.write(f"**Actual Floor Size:** {actual_width:.1f} ft x {actual_length:.1f} ft ({total_sqft:.1f} sqft)")
st.write(f"**Panels Needed:** {cols} columns x {rows} rows = {total_panels} panels")
st.write(f"**Total Cost:** ${total_cost:.2f}")

# Initialize the grid in session state if not already set.
if "pattern_grid" not in st.session_state:
    # 0 for white (opaque), 1 for black (mirror)
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

st.write("### Click on a panel to toggle its color:")

# Define Unicode squares for display
WHITE_SQUARE = "⬜"
BLACK_SQUARE = "⬛"

changed = False  # flag to trigger a re-run when any panel is clicked

# Create a grid of buttons using st.columns
for r in range(rows):
    cols_container = st.columns(cols)
    for c in range(cols):
        # Set label based on the panel's current state.
        label = WHITE_SQUARE if st.session_state.pattern_grid[r, c] == 0 else BLACK_SQUARE
        if cols_container[c].button(label, key=f"panel_{r}_{c}"):
            st.session_state.pattern_grid[r, c] = 1 - st.session_state.pattern_grid[r, c]
            changed = True

# If any panel was toggled, re-run the app to update the grid display.
if changed:
    st.experimental_rerun()

# Count the panels
opaque_count = int(np.count_nonzero(st.session_state.pattern_grid == 0))
mirror_count = int(np.count_nonzero(st.session_state.pattern_grid == 1))

st.write("### Panel Totals:")
st.write(f"- **White Panels (Opaque):** {opaque_count}")
st.write(f"- **Black Panels (Mirror):** {mirror_count}")
