import streamlit as st
import numpy as np
import math

st.title("🪩 LED Dance Floor Designer – Panel Grid")

# --------------------------
# Custom CSS for a flush, compact grid with even spacing
# --------------------------
st.markdown("""
<style>
/* Grid container styling */
.panel-grid {
    overflow-x: auto;
    white-space: nowrap;
}

/* Force columns within the grid to display inline with no wrapping */
.panel-grid .stColumns {
    display: inline-flex !important;
    flex-wrap: nowrap !important;
}

/* Style the buttons within the grid */
.panel-grid div.stButton > button {
    margin: 2px !important;         /* Even 2px gap on all sides */
    padding: 0 !important;
    width: 46px !important;          /* 46px + 2px margins ≈ 50px total */
    height: 46px !important;
    border: 1px solid #ddd !important;
    font-size: 32px !important;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

# ===== Input Section =====
st.markdown("## Floor & Cost Details")
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20, help="Enter the width in feet.")
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20, help="Enter the length in feet.")

# Panel dimensions and cost settings
panel_size_ft = 20 / 12  # 20 inches in feet (~1.667 ft)
cost_per_sqft = 15

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

# ===== Grid Initialization =====
# Reinitialize the grid if it doesn't exist or if dimensions changed.
if "pattern_grid" not in st.session_state or st.session_state.pattern_grid.shape != (rows, cols):
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

# ===== Pattern Controls (outside grid container) =====
st.markdown("## Pattern Controls")
control_cols = st.columns(2)
if control_cols[0].button("Reset Pattern"):
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)
if control_cols[1].button("Make Checkered Pattern"):
    st.session_state.pattern_grid = np.fromfunction(lambda r, c: (r + c) % 2, (rows, cols), dtype=int)

# ===== Panel Key (above totals and grid) =====
st.markdown("## Panel Key")
st.markdown("- **⬜ White:** Opaque Panel")
st.markdown("- **⬛ Black:** Mirror Panel")

# ===== Panel Totals & Cases (above the grid) =====
opaque_count = int(np.count_nonzero(st.session_state.pattern_grid == 0))
mirror_count = int(np.count_nonzero(st.session_state.pattern_grid == 1))
total_count = opaque_count + mirror_count

cases_opaque = math.ceil(opaque_count / 10)
cases_mirror = math.ceil(mirror_count / 10)
cases_total = math.ceil(total_count / 10)

st.markdown("## Panel Totals")
st.write(f"**White Panels (Opaque):** {opaque_count} — **Cases Needed:** {cases_opaque}")
st.write(f"**Black Panels (Mirror):** {mirror_count} — **Cases Needed:** {cases_mirror}")
st.write(f"**Total Panels:** {total_count} — **Total Cases Needed:** {cases_total}")

# ===== Panel Grid Section =====
st.markdown("## Panel Grid (Click a panel to toggle its color)")
# Wrap the entire grid in a container with class "panel-grid"
st.markdown(f'<div class="panel-grid">', unsafe_allow_html=True)
for r in range(rows):
    # Each row is forced to be inline-flex so that cells don't wrap:
    st.markdown('<div style="display: inline-flex; white-space: nowrap;">', unsafe_allow_html=True)
    row_cols = st.columns(cols)
    for c in range(cols):
        label = "⬜" if st.session_state.pattern_grid[r, c] == 0 else "⬛"
        if row_cols[c].button(label, key=f"panel_{r}_{c}", help=f"Row {r+1}, Col {c+1}"):
            st.session_state.pattern_grid[r, c] = 1 - st.session_state.pattern_grid[r, c]
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
