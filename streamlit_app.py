import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

st.set_page_config(page_title="Eye Tracking Heatmap", layout="centered")

st.title("🔥 Eye-Tracking Heatmap Generator")
st.write("Upload a design/poster to simulate user attention.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def generate_heatmap(img):
    img = img.convert("RGBA")
    heat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(heat)

    w, h = img.size

    # Simulated attention hotspots (can be improved later)
    hotspots = [
        (w*0.5, h*0.15, 200),   # Title
        (w*0.8, h*0.2, 150),    # Badge
        (w*0.65, h*0.4, 180),   # Section header
        (w*0.45, h*0.55, 160),  # Content/table
        (w*0.75, h*0.85, 180),  # Price/CTA
        (w*0.2, h*0.85, 120)    # Contact info
    ]

    for x, y, r in hotspots:
        bbox = [x-r, y-r, x+r, y+r]
        draw.ellipse(bbox, fill=(255, 0, 0, 120))

    heat = heat.filter(ImageFilter.GaussianBlur(100))
    combined = Image.alpha_composite(img, heat)

    return combined

if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_column_width=True)

    heatmap = generate_heatmap(image)

    st.subheader("Heatmap Result")
    st.image(heatmap, use_column_width=True)

    # Download button
    import io
    buf = io.BytesIO()
    heatmap.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Heatmap",
        data=byte_im,
        file_name="heatmap.png",
        mime="image/png"
    )
