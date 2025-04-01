import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.title("🪩 LED Dance Floor Calculator")

# User inputs
width_ft = st.number_input("Dance Floor Width (ft)", min_value=1, value=20)
length_ft = st.number_input("Dance Floor Length (ft)", min_value=1, value=20)

# Constants
panel_size_inch = 20
panel_size_ft = panel_size_inch / 12  # Convert to feet
cost_per_sqft = 10  # $10 per sqft

# Calculate panels needed
cols = math.ceil(width_ft / panel_size_ft)
rows = math.ceil(length_ft / panel_size_ft)
total_panels = cols * rows

# Actual floor size
actual_width = cols * panel_size_ft
actual_length = rows * panel_size_ft
total_sqft = actual_width * actual_length
total_cost = total_sqft * cost_per_sqft

# Display results
st.write(f"### 📏 Actual Size: {actual_width:.1f} ft x {actual_length:.1f} ft")
st.write(f"### 🔢 Panel Configuration: {cols} panels (width) x {rows} panels (length)")
st.write(f"### 🪞 Total Panels Needed: {total_panels}")
st.write(f"### 📐 Total Square Footage: {total_sqft:.1f} sqft")
st.write(f"### 💲 Total Cost: ${total_cost:.2f}")

# Visualize checkered pattern
fig, ax = plt.subplots(figsize=(cols * 0.5, rows * 0.5))

for i in range(cols):
    for j in range(rows):
        x = i * panel_size_ft
        y = j * panel_size_ft
        color = 'black' if (i + j) % 2 == 0 else 'lightgray'
        rect = patches.Rectangle((x, y), panel_size_ft, panel_size_ft,
                                 edgecolor='white', facecolor=color, lw=1)
        ax.add_patch(rect)

ax.set_xlim(0, actual_width)
ax.set_ylim(0, actual_length)
ax.set_aspect('equal')
ax.axis('off')
plt.title("Dance Floor Pattern (Mirror/Opaque)")

st.pyplot(fig)
