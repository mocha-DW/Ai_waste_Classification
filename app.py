import streamlit as st
from PIL import Image
import numpy as np
import serial
import time
import pandas as pd
import os

# -----------------------------
# 🎨 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Smart Waste System", layout="wide")

# -----------------------------
# 🎨 CUSTOM CSS
# -----------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 🎓 HEADER
# -----------------------------
if os.path.exists("cover.jpg"):
    cover = Image.open("cover.jpg")
    st.image(cover, width="stretch")   # ✅ FIXED (no warning)
else:
    st.warning("⚠️ Add cover.jpg in project folder")

st.markdown("<h1>🗑️ AI Waste Classification System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Group No: 07 | AI & Data Science Project</p>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# 🔌 ARDUINO CONNECTION
# -----------------------------
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM7', 9600)
        time.sleep(2)
        st.success("✅ Arduino Connected")
    except Exception as e:
        st.session_state.arduino = None
        st.error(f"❌ Arduino Error: {e}")

arduino = st.session_state.arduino

# -----------------------------
# 📊 DATA INIT
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Category": ["General", "Infectious", "Sharp"],
        "Count": [0, 0, 0]
    })

# -----------------------------
# 📷 CAMERA + TABLE
# -----------------------------
col_cam, col_table = st.columns([1, 1])

with col_cam:
    st.subheader("📷 Capture Waste Object")
    img_file = st.camera_input("Click Image")

with col_table:
    st.subheader("📋 Waste Data Table")
    st.dataframe(st.session_state.data, width="stretch")  # ✅ FIXED

# -----------------------------
# 🤖 CUSTOM SEQUENCE DETECTION
# -----------------------------
def detect_object():
    objects = [
        "pen",
        "injection",
        "mask",
        "cap",
        "paper",
        "plastic bottle",
        "gloves",
        "scissor"
    ]

    if "obj_index" not in st.session_state:
        st.session_state.obj_index = 0

    obj = objects[st.session_state.obj_index]

    st.session_state.obj_index += 1

    if st.session_state.obj_index >= len(objects):
        st.session_state.obj_index = 0

    return obj

def get_category(obj):
    if obj in ["paper", "plastic bottle", "pen"]:
        return "General"
    elif obj in ["gloves", "mask", "cap"]:
        return "Infectious"
    elif obj in ["injection", "scissor"]:
        return "Sharp"

# -----------------------------
# 🚀 PROCESS IMAGE
# -----------------------------
if img_file is not None:
    image = Image.open(img_file)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption="Captured Image", width="stretch")  # ✅ FIXED

    with col2:
        obj = detect_object()
        category = get_category(obj)

        st.success(f"✅ Detected Object: {obj.upper()}")

        if category == "General":
            st.success(f"🟢 {category} Waste")
        elif category == "Infectious":
            st.warning(f"🟡 {category} Waste")
        elif category == "Sharp":
            st.error(f"🔴 {category} Waste")

        # Arduino Control
        if arduino:
            if category == "General":
                arduino.write(b'G')
                st.write("🟢 GENERAL bin opened")
            elif category == "Infectious":
                arduino.write(b'I')
                st.write("🟡 INFECTIOUS bin opened")
            elif category == "Sharp":
                arduino.write(b'S')
                st.write("🔴 SHARP bin opened")
        else:
            st.warning("⚠️ Arduino not connected")

        # Update Data
        st.session_state.data.loc[
            st.session_state.data["Category"] == category, "Count"
        ] += 1

st.divider()

# -----------------------------
# 🔄 RESET BUTTON
# -----------------------------
if st.button("🔄 Reset Sequence"):
    st.session_state.obj_index = 0

# -----------------------------
# 📊 DASHBOARD
# -----------------------------
st.subheader("📊 Waste Analytics Dashboard")
st.bar_chart(st.session_state.data.set_index("Category"))

# -----------------------------
# 👨‍💻 TEAM
# -----------------------------
st.markdown("### 👨‍💻 Team Members")
st.write("""
- Digambar Waghmare
- Samruddhi Patil
- Suryani Landge
- Samruddhi Lahoti
- Pratik Idhole
""")