# app.py
import streamlit as st
import requests
import matplotlib.pyplot as plt

# --- Page setup ---
st.set_page_config(page_title="🎨 Color Palette Generator (API)", page_icon="🎨", layout="centered")
st.title("🎨 Color Palette Generator with TheColorAPI")
st.caption("Genera una paleta de colores conectada a una API real, usando una clave secreta (API KEY).")

# --- API Key Verification ---
st.subheader("🔑 Acceso con API Key")

user_key = st.text_input("Introduce tu API Key:", type="password")

# Secret key stored in Streamlit
SECRET_KEY = st.secrets["colorapi"]["API_KEY"]

if user_key == "":
    st.info("👆 Ingresa tu API key para continuar.")
elif user_key != SECRET_KEY:
    st.error("❌ Clave incorrecta.")
else:
    st.success("✅ Clave correcta. ¡Bienvenido al generador de paletas!")

    st.markdown("---")
    st.subheader("🎨 Genera una paleta desde un color base")

    base_color = st.color_picker("Elige un color base:", "#FF5733")
    count = st.slider("Número de colores en la paleta:", 3, 8, 5)

    # Convertir color HEX a formato sin #
    color_hex = base_color.replace("#", "")

    # Llamada a TheColorAPI
    url = f"https://www.thecolorapi.com/scheme?hex={color_hex}&mode=analogic&count={count}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        colors = [c["hex"]["value"] for c in data["colors"]]

        # Mostrar paleta
        st.subheader("🌈 Paleta generada desde TheColorAPI")
        fig, ax = plt.subplots(figsize=(8, 2))
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.set_xlim(0, len(colors))
        ax.set_ylim(0, 1)
        ax.axis("off")
        st.pyplot(fig)

        # Mostrar códigos de color
        st.subheader("🧾 Códigos de color (HEX)")
        cols = st.columns(len(colors))
        for i, color in enumerate(colors):
            with cols[i]:
                st.markdown(f"**{color}**")
                st.color_picker("", color, key=i)
    else:
        st.error("Error al conectar con TheColorAPI. Intenta más tarde.")
