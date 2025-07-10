
import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd
import io
import datetime

st.set_page_config(page_title="QR Attendance (Cloud)", layout="centered")
st.title("📸 QR Attendance System (Camera Supported)")
st.caption("Scan QR code using your device camera.")

# Load or initialize attendance data
try:
    attendance_df = pd.read_excel("attendance.xlsx")
except FileNotFoundError:
    attendance_df = pd.DataFrame(columns=[
        "Enrollment no", "Name", "Email", "Mobile", "Address",
        "Father Name", "DOB", "Status", "Coupon Code", "Timestamp"
    ])

# Helper to parse QR content
def parse_qr_data(data):
    info = {}
    for line in data.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
    return info

# Capture photo via camera
img_file = st.camera_input("📷 Take Photo to Scan QR Code")

if img_file is not None:
    image = Image.open(img_file)
    decoded_objs = decode(image)

    if decoded_objs:
        qr_data = decoded_objs[0].data.decode('utf-8')
        info = parse_qr_data(qr_data)

        st.success("QR Code Scanned Successfully!")
        st.json(info)

        status = st.radio("Mark Attendance", ("Present", "Absent"))
        coupon = st.text_input("🎟️ Enter Coupon Code (optional)")

        if st.button("✅ Submit"):
            info["Status"] = status
            info["Coupon Code"] = coupon
            info["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance_df.loc[len(attendance_df)] = info
            attendance_df.to_excel("attendance.xlsx", index=False)
            st.success("Attendance marked and saved!")
    else:
        st.error("No valid QR code found in the image.")

# Show attendance log
if st.checkbox("📄 Show Attendance Log"):
    st.dataframe(attendance_df)
