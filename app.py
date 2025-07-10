import streamlit as st
import cv2
import pandas as pd
import tempfile
import datetime

st.set_page_config(page_title="QR Attendance (OpenCV)", layout="centered")
st.title("📸 QR Attendance System (OpenCV-based)")

# Load or initialize attendance data
try:
    attendance_df = pd.read_excel("attendance.xlsx")
except FileNotFoundError:
    attendance_df = pd.DataFrame(columns=[
        "Enrollment no", "Name", "Email", "Mobile", "Address",
        "Father Name", "DOB", "Status", "Timestamp"
    ])

def parse_qr_data(data):
    info = {}
    for line in data.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
    return info

uploaded_file = st.file_uploader("📂 Upload QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        img_path = tmp_file.name

    image = cv2.imread(img_path)
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)

    if data:
        info = parse_qr_data(data)
        st.success("QR Code Scanned Successfully!")
        st.json(info)

        status = st.radio("Mark Attendance", ("Present", "Absent"))

        if st.button("✅ Submit"):
            info["Status"] = status
            info["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance_df.loc[len(attendance_df)] = info
            attendance_df.to_excel("attendance.xlsx", index=False)
            st.success("Attendance marked and saved!")
    else:
        st.error("No QR code detected in the image.")

if st.checkbox("📄 Show Attendance Log"):
    st.dataframe(attendance_df)
