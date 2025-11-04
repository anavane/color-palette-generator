# app.py
import streamlit as st
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import matplotlib.pyplot as plt

st.set_page_config(page_title="🎨 Color Palette Generator", page_icon="🎨", layout="centered")

st.title("🎨 Color Palette Generator from Artwork")
st.caption("Sube una imagen (pintura, ilustración o fotografía) y descubre su paleta de colores principales.")

# --- Upload image ---
uploaded_file = st.file_uploader("📁 Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Mostrar imagen original
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    # Convertir imagen a formato que pueda leer ColorThief
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Extraer colores
    color_thief = ColorThief(img_bytes)
    palette = color_thief.get_palette(color_count=6)

    st.subheader("🎨 Paleta de colores principal")

    # Mostrar paleta
    fig, ax = plt.subplots(figsize=(8, 2))
    for i, color in enumerate(palette):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=[c/255 for c in color]))
    ax.set_xlim(0, len(palette))
    ax.set_ylim(0, 1)
    ax.axis("off")
    st.pyplot(fig)

    # Mostrar códigos RGB/HEX
    st.subheader("🧾 Códigos de color")
    cols = st.columns(len(palette))
    for i, color in enumerate(palette):
        r, g, b = color
        hex_code = '#%02x%02x%02x' % (r, g, b)
        with cols[i]:
            st.markdown(f"**{hex_code.upper()}**")
            st.markdown(f"RGB: ({r}, {g}, {b})")
            st.color_picker("", hex_code, key=i)
else:
    st.info("👆 Sube una imagen para generar la paleta de colores.")
