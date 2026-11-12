
import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Hire Caretakers | Krishi Saarthi",
    page_icon="👨‍🌾",
    layout="wide"
)

st.title("👨‍🌾 Hire Farm Caretakers")
st.caption("Find support to manage your agricultural land.")

# Database setup
conn = sqlite3.connect("krishi_saarthi.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hiring_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_name TEXT,
    phone TEXT,
    location TEXT,
    land_area REAL,
    crop TEXT,
    package TEXT,
    requirements TEXT,
    request_date TEXT
)
""")

conn.commit()

# Sample caretaker profiles
caretakers = [
    {
        "name": "Rajesh Kumar",
        "experience": "5 Years",
        "speciality": "Wheat, Rice",
        "location": "Punjab",
        "services": "Irrigation, Crop Monitoring",
        "package": "Monthly"
    },
    {
        "name": "Aman Singh",
        "experience": "3 Years",
        "speciality": "Vegetables, Tomato",
        "location": "Punjab",
        "services": "Plant Care, Fertilizer Management",
        "package": "Seasonal"
    },
    {
        "name": "Gurpreet Singh",
        "experience": "7 Years",
        "speciality": "Mixed Farming",
        "location": "Punjab",
        "services": "Farm Supervision, Field Management",
        "package": "Monthly"
    }
]

st.info(
    "The caretaker profiles below are sample demonstration profiles, "
    "not verified real service providers."
)

# Caretaker profiles
st.subheader("🌱 Available Caretaker Profiles")

cols = st.columns(3)

for i, caretaker in enumerate(caretakers):

    with cols[i]:

        with st.container(border=True):

            st.subheader(f"👨‍🌾 {caretaker['name']}")

            st.write(f"📍 Location: {caretaker['location']}")
            st.write(f"⭐ Experience: {caretaker['experience']}")
            st.write(f"🌾 Speciality: {caretaker['speciality']}")
            st.write(f"🛠️ Services: {caretaker['services']}")
            st.write(f"📅 Package: {caretaker['package']}")

            st.caption("Demo profile – verification pending")


st.divider()

# Services
st.subheader("🛠️ Available Farming Services")

services = [
    ("🌱 Crop Monitoring", "Regular observation of crop growth."),
    ("💧 Irrigation Management", "Help with planning field irrigation."),
    ("🌾 Field Supervision", "General farm activity supervision."),
    ("🌿 Plant Care", "Basic crop and plant maintenance."),
    ("🚜 Farm Management", "Assistance with routine farm operations.")
]

for name, description in services:
    st.markdown(f"**{name}**")
    st.write(description)

st.divider()

# Hiring form
st.subheader("📝 Submit a Hiring Enquiry")

with st.form("hiring_form"):

    col1, col2 = st.columns(2)

    with col1:

        farmer_name = st.text_input("Farmer Name")

        phone = st.text_input(
            "Contact Number",
            max_chars=15
        )

        location = st.text_input(
            "Farm Location / District"
        )

        land_area = st.number_input(
            "Land Area (Acres)",
            min_value=0.1,
            value=2.0
        )

    with col2:

        crop = st.selectbox(
            "Main Crop",
            [
                "Wheat",
                "Rice",
                "Vegetables",
                "Fruits",
                "Cotton",
                "Sugarcane",
                "Mixed Farming",
                "Other"
            ]
        )

        package = st.selectbox(
            "Required Package",
            [
                "Daily",
                "Monthly",
                "Seasonal",
                "Custom"
            ]
        )

        caretaker_choice = st.selectbox(
            "Preferred Caretaker",
            ["No Preference"] +
            [c["name"] for c in caretakers]
        )

    requirements = st.text_area(
        "Additional Requirements",
        placeholder="Describe the work you need help with..."
    )

    submitted = st.form_submit_button(
        "📩 Submit Hiring Enquiry",
        use_container_width=True
    )


if submitted:

    if not farmer_name.strip():
        st.warning("Please enter your name.")

    elif not phone.strip() or not phone.strip().replace("+", "").isdigit():
        st.warning("Please enter a valid contact number.")

    elif not location.strip():
        st.warning("Please enter your farm location.")

    else:

        cursor.execute("""
        INSERT INTO hiring_requests (
            farmer_name,
            phone,
            location,
            land_area,
            crop,
            package,
            requirements,
            request_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            farmer_name.strip(),
            phone.strip(),
            location.strip(),
            land_area,
            crop,
            package,
            requirements.strip(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        st.success(
            "Your hiring enquiry has been saved successfully!"
        )

        st.info(
            "This is a prototype enquiry system. "
            "No caretaker has been contacted or booked."
        )


# Admin/demo enquiry view
st.divider()

with st.expander("🔐 Demo: View Hiring Enquiries"):

    cursor.execute("""
        SELECT id, farmer_name, location, crop, package, request_date
        FROM hiring_requests
        ORDER BY id DESC
    """)

    requests = cursor.fetchall()

    if requests:
        st.dataframe(
            requests,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hiring enquiries submitted yet.")

conn.close()

st.divider()
st.caption("KRISHI SAARTHI | Farm Workforce Management")
