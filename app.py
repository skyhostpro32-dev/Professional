import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# USAGE LIMIT SYSTEM
# =========================
FREE_LIMIT = 4

if "usage" not in st.session_state:
    st.session_state.usage = {
        "bg": 0,
        "enhance": 0,
        "erase": 0,
        "blur": 0,
        "remove": 0,
        "bg_tool": 0
    }

# =========================
# PAYMENT FUNCTION
# =========================
def show_payment(tool_name):
    st.warning(f"🔒 {tool_name} limit reached (4 free uses)")
    st.markdown("### 💳 Upgrade to Pro")
    st.link_button(
        "💳 Pay ₹99 to Unlock",
        "https://rzp.io/l/YOUR_PAYMENT_LINK"
    )

# =========================
# CSS
# =========================
st.markdown("""
<style>

/* Hide Streamlit UI */
header, #MainMenu, footer {visibility: hidden;}
div[data-testid="stToolbar"], div[data-testid="stDeployButton"] {
    display:none !important;
}

/* Background */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
}

/* Title */
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #5b21b6;
}

/* Tool Card */
.tool-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e9d5ff;
    height: 140px;
    transition: 0.25s;
}
.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(139,92,246,0.15);
}

/* Invisible Button */
.stButton > button {
    width: 100%;
    height: 140px;
    opacity: 0;
    position: absolute;
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="main-title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
uploaded_file = st.sidebar.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])

# =========================
# TOOL CARDS
# =========================
st.subheader("🧰 Choose a Tool")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("", key="bg"):
        st.session_state.tool = "bg"
    st.markdown('<div class="tool-card">🎨<br>Background Change</div>', unsafe_allow_html=True)

with col2:
    if st.button("", key="enhance"):
        st.session_state.tool = "enhance"
    st.markdown('<div class="tool-card">✨<br>Enhance Image</div>', unsafe_allow_html=True)

with col3:
    if st.button("", key="erase"):
        st.session_state.tool = "erase"
    st.markdown('<div class="tool-card">🧽<br>Erase Tool</div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("", key="blur"):
        st.session_state.tool = "blur"
    st.markdown('<div class="tool-card">🌫<br>Blur Tool</div>', unsafe_allow_html=True)

with col5:
    if st.button("", key="remove"):
        st.session_state.tool = "remove"
    st.markdown('<div class="tool-card">❌<br>Remove Object</div>', unsafe_allow_html=True)

with col6:
    if st.button("", key="bg_tool"):
        st.session_state.tool = "bg_tool"
    st.markdown('<div class="tool-card">🖼<br>Background Tool</div>', unsafe_allow_html=True)

# =========================
# IMAGE PROCESSING
# =========================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    colA, colB = st.columns(2)

    with colA:
        st.image(image, caption="Original")

    tool = st.session_state.get("tool")

    # 🎨 BACKGROUND
    if tool == "bg":
        if st.session_state.usage["bg"] >= FREE_LIMIT:
            show_payment("Background Tool")
        else:
            color_hex = st.color_picker("Pick Color", "#8b5cf6")
            color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

            if st.button("Apply"):
                st.session_state.usage["bg"] += 1

                arr = np.array(image)
                mask = np.mean(arr, axis=2) > 200
                arr[mask] = color
                result = Image.fromarray(arr)

                with colB:
                    st.image(result)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "bg.png")

    # ✨ ENHANCE
    elif tool == "enhance":
        if st.session_state.usage["enhance"] >= FREE_LIMIT:
            show_payment("Enhance Tool")
        else:
            strength = st.slider("Sharpness", 1, 5, 2)

            if st.button("Enhance"):
                st.session_state.usage["enhance"] += 1

                result = image
                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

                with colB:
                    st.image(result)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button("Download", buf.getvalue(), "enhanced.png")

    # 🔗 LINK TOOLS
    elif tool == "erase":
        if st.session_state.usage["erase"] >= FREE_LIMIT:
            show_payment("Erase Tool")
        else:
            st.session_state.usage["erase"] += 1
            st.link_button("Open Erase Tool", "https://skyhostpro32-dev.github.io/erase-tool/")

    elif tool == "blur":
        if st.session_state.usage["blur"] >= FREE_LIMIT:
            show_payment("Blur Tool")
        else:
            st.session_state.usage["blur"] += 1
            st.link_button("Open Blur Tool", "https://skyhostpro32-dev.github.io/index./")

    elif tool == "remove":
        if st.session_state.usage["remove"] >= FREE_LIMIT:
            show_payment("Remove Tool")
        else:
            st.session_state.usage["remove"] += 1
            st.link_button("Open Remove Tool", "https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

    elif tool == "bg_tool":
        if st.session_state.usage["bg_tool"] >= FREE_LIMIT:
            show_payment("Background Tool")
        else:
            st.session_state.usage["bg_tool"] += 1
            st.link_button("Open Background Tool", "https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

else:
    st.info("👈 Upload an image to start")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Pro Version Available")
