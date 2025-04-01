import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import math
from PIL import Image, ImageDraw
import io
import base64

st.title("🪩 LED Dance Floor Designer (Interactive)")

# Inputs
width_ft = st.number_input("Width (ft)", min_value=1, value=20)
length_ft = st.number_input("Length (ft)", min_value=1, value=20)

panel_size_ft = 20 / 12
cols = math.ceil(width_ft / panel_size_ft)
rows = math.ceil(length_ft / panel_size_ft)

actual_width = cols * panel_size_ft
actual_length = rows * panel_size_ft
total_sqft = actual_width * actual_length
total_cost = total_sqft * 15

st.write(f"**Actual Size:** {actual_width:.1f} x {actual_length:.1f} ft ({total_sqft:.1f} sqft)")
st.write(f"**Panels Needed:** {cols} x {rows} = {cols*rows} panels")
st.write(f"**Total Cost:** ${total_cost:.2f}")

# Canvas setup
canvas_size = 600
cell_w = canvas_size // cols
cell_h = canvas_size // rows

# Reset pattern if needed
if 'pattern_grid' not in st.session_state or st.button("Reset Pattern"):
    st.session_state.pattern_grid = np.zeros((rows, cols), dtype=int)

# Function to generate grid image
def create_grid_image(grid):
    img = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(img)
    for r in range(rows):
        for c in range(cols):
            color = 'gray' if grid[r, c] == 0 else 'black'
            draw.rectangle([c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h], fill=color, outline='white')
    return img

# Function to convert PIL image to data URL
def pil_to_data_url(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return "data:image/png;base64," + img_str

# Create grid image and convert to data URL
bg_img = create_grid_image(st.session_state.pattern_grid)
bg_data_url = pil_to_data_url(bg_img)

st.write("### 🖱️ Click on panels to toggle Mirror/Opaque:")

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 1)",
    stroke_width=1,
    stroke_color="white",
    background_image=bg_data_url,  # Use our manually generated data URL
    update_streamlit=True,
    height=canvas_size,
    width=canvas_size,
    drawing_mode="point",
    key="canvas",
)

# Process clicks to toggle panel types
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data["objects"]:
        x = int(obj["left"] // cell_w)
        y = int(obj["top"] // cell_h)
        if 0 <= y < rows and 0 <= x < cols:
            st.session_state.pattern_grid[y, x] = 1 - st.session_state.pattern_grid[y, x]

opaque_count = np.count_nonzero(st.session_state.pattern_grid == 0)
mirror_count = np.count_nonzero(st.session_state.pattern_grid == 1)

st.write(f"🪞 **Mirror Panels:** {mirror_count}")
st.write(f"⬜ **Opaque Panels:** {opaque_count}")
