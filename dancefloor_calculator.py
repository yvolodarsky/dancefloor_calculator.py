import streamlit as st
import numpy as np
import math

st.title("🪩 LED Dance Floor Designer")

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

# Initialize or reset the grid pattern in session state if not already done.
if 'pattern_grid' not in st.session_state:
    # 0 represents Opaque (gray) and 1 represents Mirror (black)
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

st.write("### Click on each panel to toggle between Opaque and Mirror.")

rerun_needed = False  # Flag to indicate if we need to rerun the script

# Create the grid of buttons
for r in range(rows):
    # Create a row of columns (buttons)
    cols_container = st.columns(cols)
    for c in range(cols):
        # Determine the button label and color based on current state
        if st.session_state.pattern_grid[r, c] == 0:
            label = "Opaque"
            button_color = "#d3d3d3"  # light gray
        else:
            label = "Mirror"
            button_color = "#000000"  # black

        # Style the button using HTML within Markdown
        button_html = f"""
        <div style="background-color:{button_color}; padding:10px; text-align:center; border-radius:5px;">
            <span style="color:{'white' if st.session_state.pattern_grid[r, c]==1 else 'black'}">{label}</span>
        </div>
        """
        # Create the button with a unique key for each cell
        if cols_container[c].button(button_html, key=f"cell_{r}_{c}", help=f"Row {r+1}, Col {c+1}"):
            # Toggle the panel type when the button is clicked
            st.session_state.pattern_grid[r, c] = 1 - st.session_state.pattern_grid[r, c]
            rerun_needed = True

# If any cell was toggled, rerun the app once after the loop
if rerun_needed:
    st.experimental_rerun()

# After the grid, display the counts of each panel type
opaque_count = int(np.count_nonzero(st.session_state.pattern_grid == 0))
mirror_count = int(np.count_nonzero(st.session_state.pattern_grid == 1))

st.write("### Panel Totals:")
st.write(f"- **Opaque Panels:** {opaque_count}")
st.write(f"- **Mirror Panels:** {mirror_count}")
