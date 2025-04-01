import streamlit as st
import numpy as np
import math

st.title("🪩 LED Dance Floor Designer – Panel Grid")

# ===== Input Section =====
st.markdown("## Floor & Cost Details")
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20, help="Enter the width in feet.")
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20, help="Enter the length in feet.")

# Panel dimensions and cost settings
panel_size_ft = 20 / 12  # 20 inches converted to feet (approx. 1.667 ft)
cost_per_sqft = 15

# Calculate grid dimensions
cols = math.ceil(width_ft / panel_size_ft)
rows = math.ceil(length_ft / panel_size_ft)
total_panels = cols * rows

# Actual floor size (rounded up to panels)
actual_width = cols * panel_size_ft
actual_length = rows * panel_size_ft
total_sqft = actual_width * actual_length
total_cost = total_sqft * cost_per_sqft

st.write(f"**Actual Floor Size:** {actual_width:.1f} ft x {actual_length:.1f} ft ({total_sqft:.1f} sqft)")
st.write(f"**Panels Needed:** {cols} columns x {rows} rows = {total_panels} panels")
st.write(f"**Total Cost:** ${total_cost:.2f}")

# ===== Panel Grid Section =====
st.markdown("## Panel Grid (Click a panel to toggle its color)")
# Initialize or reset the grid pattern in session state if not already done, or if dimensions have changed.
if "pattern_grid" not in st.session_state or st.session_state.pattern_grid.shape != (rows, cols):
    # 0 = White (Opaque), 1 = Black (Mirror)
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

# Unicode symbols for display
WHITE_SQUARE = "⬜"
BLACK_SQUARE = "⬛"

st.write("### Click on a panel to toggle its color:")

# Create the grid using st.columns()
for r in range(rows):
    cols_container = st.columns(cols)
    for c in range(cols):
        # Access the cell safely now that the grid shape matches the current rows, cols.
        label = WHITE_SQUARE if st.session_state.pattern_grid[r, c] == 0 else BLACK_SQUARE
        if cols_container[c].button(label, key=f"panel_{r}_{c}", help=f"Row {r+1}, Col {c+1}"):
            st.session_state.pattern_grid[r, c] = 1 - st.session_state.pattern_grid[r, c]

# ===== Totals & Cases Section =====
opaque_count = int(np.count_nonzero(st.session_state.pattern_grid == 0))
mirror_count = int(np.count_nonzero(st.session_state.pattern_grid == 1))
total_count = opaque_count + mirror_count  # should equal total_panels

# Calculate cases needed (10 panels per case)
cases_opaque = math.ceil(opaque_count / 10)
cases_mirror = math.ceil(mirror_count / 10)
cases_total = math.ceil(total_count / 10)

st.markdown("## Panel Totals")
st.write(f"**White Panels (Opaque):** {opaque_count}  —  **Cases Needed:** {cases_opaque}")
st.write(f"**Black Panels (Mirror):** {mirror_count}  —  **Cases Needed:** {cases_mirror}")
st.write(f"**Total Panels:** {total_count}  —  **Total Cases Needed:** {cases_total}")

# ===== Key Section =====
st.markdown("## Panel Key")
st.markdown("- **⬜ White:** Opaque Panel")
st.markdown("- **⬛ Black:** Mirror Panel")
