import streamlit as st
from image_generator import generate_image
from utils import split_prompts
from PIL import Image
import io
import zipfile
import tempfile
import base64

st.set_page_config(page_title="🎨 Text-to-Image Storyboard", layout="wide")

# Styling
st.markdown("""
    <style>
        .main-title {
            font-size: 42px;
            font-weight: bold;
            background: -webkit-linear-gradient(90deg, #ff6ec4, #7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            text-align: center;
            width: 100%;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🖼️ Text-to-Image Storyboard</div>", unsafe_allow_html=True)
st.markdown("Generate stunning visuals from your imagination!")

# Input / Output Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Enter Your Storyboard Prompts")
    multiline_prompts = st.text_area(
        "Describe each scene (one per line)",
        height=200,
        placeholder="e.g. A spaceship landing on Mars\nA robot walking in a neon-lit alley..."
    )

    with st.expander("⚙️ Advanced Options"):
        style = st.selectbox("Image Style", ["Realistic", "Anime", "Cyberpunk", "Sketch"])
        resolution = st.radio("Resolution", ["512x512", "768x768"], horizontal=True)

    if st.button("🎬 Generate Storyboard"):
        prompts = split_prompts(multiline_prompts)
        if prompts:
            with st.spinner("Generating storyboard images..."):
                images = []
                for i, prompt in enumerate(prompts):
                    st.write(f"**Scene {i+1}:** {prompt}")
                    try:
                        image_bytes = generate_image(prompt, style, resolution)
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, use_container_width=True)
                        images.append((f"scene_{i+1}.png", image_bytes))
                    except Exception as e:
                        st.error(f"Error generating image for Scene {i+1}: {e}")

                st.session_state['images'] = images

                st.markdown("### 🎞️ Storyboard Preview")
                cols = st.columns(len(images))

                for i, ((filename, img_bytes), col, prompt) in enumerate(zip(images, cols, prompts)):
                    with col:
                        img = Image.open(io.BytesIO(img_bytes))
                        col.image(img, caption=f"Scene {i+1}", use_container_width=True)
                        col.markdown(f"<div style='text-align: center; font-size: 12px;'>{prompt}</div>", unsafe_allow_html=True)

                # ZIP Download
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zipf:
                        for filename, img_bytes in images:
                            zipf.writestr(filename, img_bytes)

                with open(tmp_zip.name, "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()

                href = f'<a href="data:application/zip;base64,{b64}" download="storyboard.zip">📥 Download All Images as ZIP</a>'
                st.markdown(href, unsafe_allow_html=True)

                # 🎥 Video Export
                if st.button("📽️ Export as Story Video"):
                    with st.spinner("Creating your video..."):
                        from video_generator import create_storyboard_video
                        video_path = create_storyboard_video([
                            (prompt, img_bytes) for (fname, img_bytes), prompt in zip(images, prompts)
                        ])

                    with open(video_path, "rb") as f:
                        video_bytes = f.read()
                    b64_video = base64.b64encode(video_bytes).decode()
                    video_link = f'<a href="data:video/mp4;base64,{b64_video}" download="storyboard_video.mp4">🎬 Download Story Video</a>'
                    st.markdown(video_link, unsafe_allow_html=True)
        else:
            st.warning("Please enter at least one prompt.")

with col2:
    st.subheader("🖼️ Preview Last Generated Image")
    if 'images' in st.session_state and st.session_state['images']:
        last_image = Image.open(io.BytesIO(st.session_state['images'][-1][1]))
        st.image(last_image, use_container_width=True)
    else:
        st.info("Your last generated image will appear here.")

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Ayush Mundharikar</div>", unsafe_allow_html=True)
