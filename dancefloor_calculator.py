import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np

st.title("🪩 Dynamic LED Dance Floor Designer")

# Inputs
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20)
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20)

panel_size_inch = 20
panel_size_ft = panel_size_inch / 12
cost_per_sqft = 15

cols = math.ceil(width_ft / panel_size_ft)
rows = math.ceil(length_ft / panel_size_ft)
total_panels = cols * rows

actual_width = cols * panel_size_ft
actual_length = rows * panel_size_ft
total_sqft = actual_width * actual_length
total_cost = total_sqft * cost_per_sqft

st.write(f"### 📏 Actual Size: {actual_width:.1f} ft x {actual_length:.1f} ft")
st.write(f"### 🔢 Panels: {cols} x {rows} ({total_panels} total)")
st.write(f"### 📐 Total Sqft: {total_sqft:.1f} sqft | 💲 Total Cost: ${total_cost:.2f}")

# Interactive pattern selection
pattern_types = {'Opaque (gray)': 0, 'Mirror (black)': 1}
selected_pattern = st.selectbox("Default Pattern:", list(pattern_types.keys()))

# Initialize pattern grid
pattern_grid = np.full((rows, cols), pattern_types[selected_pattern])

# Manual override (clickable pattern)
st.write("### Click Panels to Toggle Opaque/Mirror:")
toggle_positions = st.multiselect(
    "Select panels to toggle (row,col):",
    [(r, c) for r in range(rows) for c in range(cols)],
    format_func=lambda x: f"Row {x[0]+1}, Col {x[1]+1}"
)

# Toggle the selected panels
for r, c in toggle_positions:
    pattern_grid[r, c] = 1 - pattern_grid[r, c]

# Count types of panels
opaque_count = np.count_nonzero(pattern_grid == 0)
mirror_count = np.count_nonzero(pattern_grid == 1)

st.write(f"### 🪞 Mirror Panels: {mirror_count}")
st.write(f"### ⬜ Opaque Panels: {opaque_count}")

# Visualize floor pattern
fig, ax = plt.subplots(figsize=(cols * 0.5, rows * 0.5))

for r in range(rows):
    for c in range(cols):
        x = c * panel_size_ft
        y = r * panel_size_ft
        color = 'lightgray' if pattern_grid[r, c] == 0 else 'black'
        rect = patches.Rectangle((x, y), panel_size_ft, panel_size_ft,
                                 edgecolor='white', facecolor=color, lw=1)
        ax.add_patch(rect)

ax.set_xlim(0, actual_width)
ax.set_ylim(0, actual_length)
ax.set_aspect('equal')
ax.axis('off')
plt.title("Customized Dance Floor Pattern")

st.pyplot(fig)
