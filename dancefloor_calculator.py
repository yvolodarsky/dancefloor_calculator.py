import streamlit as st
import numpy as np
import math

st.title("🪩 LED Dance Floor Designer – Colored Panel Grid")

# Inputs for dance floor dimensions
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20)
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20)

# Constants: Panel size (20 inches converted to feet) and cost per square foot
panel_size_ft = 20 / 12
cost_per_sqft = 15

# Calculate grid dimensions based on the panel size
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

# Initialize or reset the grid pattern in session state if not already set.
if 'pattern_grid' not in st.session_state or st.button("Reset Pattern"):
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

# Define a callback to toggle a cell at (r, c)
def toggle_cell(r, c):
    st.session_state.pattern_grid[r, c] = 1 - st.session_state.pattern_grid[r, c]

st.write("### Click on each panel to toggle its color (White ↔ Black).")

# Create the grid of colored buttons using custom CSS styling
for r in range(rows):
    cols_container = st.columns(cols)
    for c in range(cols):
        # Determine the button's background color based on current state:
        # 0 = white (opaque), 1 = black (mirror)
        button_color = "#FFFFFF" if st.session_state.pattern_grid[r, c] == 0 else "#000000"
        # Create a unique key for the button
        button_id = f"button_cell_{r}_{c}"
        # Inject custom CSS to style the button
        st.markdown(
            f"""
            <style>
            #{button_id} button {{
                background-color: {button_color} !important;
                border: none;
                height: 50px;
                width: 50px;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Create the button with an on_click callback that toggles the cell.
        cols_container[c].button("", key=button_id, help=f"Row {r+1}, Col {c+1}", on_click=toggle_cell, args=(r, c))

# After the grid, display totals for each panel type.
opaque_count = int(np.count_nonzero(st.session_state.pattern_grid == 0))
mirror_count = int(np.count_nonzero(st.session_state.pattern_grid == 1))

st.write("### Panel Totals:")
st.write(f"- **White Panels (Opaque):** {opaque_count}")
st.write(f"- **Black Panels (Mirror):** {mirror_count}")
