
import streamlit as st

st.set_page_config(
    page_title="KRISHI SAARTHI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SERVICES ----------------

modules = [
    ("🤖", "Kisan AI", "Ask your farming questions.", "pages/1_Kisan_AI.py"),
    ("🌾", "Crop Recommendation", "Discover suitable crops.", "pages/2_Crop_Recommendation.py"),
    ("🌦️", "Weather Forecast", "Check weather conditions.", "pages/3_Weather_Forecast.py"),
    ("⏳", "Time Predictor", "Estimate harvest periods.", "pages/4_Time_Predictor.py"),
    ("🏡", "Greenhouse Planner", "Plan your greenhouse.", "pages/5_Greenhouse.py"),
    ("👨‍🌾", "Hire Caretakers", "Explore caretaker services.", "pages/6_Hire_Caretakers.py"),
    ("🧪", "Soil Health", "Understand your soil.", "pages/7_Soil_Health.py"),
    ("📈", "Live Mandi Rates", "Explore market prices.", "pages/8_Mandi_Rates.py"),
    ("🔬", "Plant Disease Detection", "Check plant health.", "pages/9_Plant_Disease.py"),
    ("🏛️", "Government Schemes", "Explore farmer schemes.", "pages/10_Government_Schemes.py")
]

# ---------------- CSS ----------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #F4F6EF;
}

/* Hide default top decoration */
[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #E8EFE5;
}

/* Headings */
h1, h2, h3 {
    color: #173F2B;
}

/* Compact hero */
.hero {
    background: linear-gradient(115deg, #123B29, #246342);
    padding: 23px 30px;
    border-radius: 17px;
    margin-bottom: 16px;
    border: 1px solid #376C4C;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 34px;
    margin: 0;
}

.hero p {
    color: #E4EDE2;
    font-size: 14px;
    margin: 5px 0 0 0;
}

.hero-tag {
    color: #E6C66F;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}

/* Top quick navigation */
.nav-label {
    color: #A47C29;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 4px 0 8px 2px;
}

/* Service cards */
.service-card {
    background: #FFFFFF;
    border: 1px solid #E0E8DD;
    border-radius: 13px;
    padding: 14px 13px;
    min-height: 125px;
    box-shadow: 0 3px 10px rgba(23, 63, 43, 0.04);
}

.service-card:hover {
    border: 1px solid #B69A4E;
    background: #FBFCF8;
}

.service-icon {
    font-size: 25px;
    margin-bottom: 5px;
}

.service-name {
    font-size: 14px;
    font-weight: 750;
    color: #17452E;
    margin-bottom: 4px;
}

.service-description {
    font-size: 11px;
    color: #748174;
    line-height: 1.35;
}

/* Buttons */
div.stButton > button,
div.stPageLink > a {
    background: #1D5739;
    color: white !important;
    border: 0;
    border-radius: 8px;
    font-size: 12px;
    min-height: 34px;
    width: 100%;
    justify-content: center;
}

div.stButton > button:hover,
div.stPageLink > a:hover {
    background: #34754D;
    color: white !important;
    border: 1px solid #D4B65D;
}

/* Top links */
div[data-testid="stHorizontalBlock"] {
    gap: 9px;
}

/* Footer */
.footer {
    text-align: center;
    color: #788477;
    font-size: 11px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🌱 KRISHI SAARTHI")
    st.caption("Your Smart Farming Companion")
    st.divider()

    st.page_link("main.py", label="Dashboard", icon="🏠")

    for icon, name, description, page in modules:
        st.page_link(page, label=name, icon=icon)

    st.divider()
    st.caption("Empowering Farmers Through Technology")


# ---------------- COMPACT HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">SMART AGRICULTURE PLATFORM</div>
    <h1>🌱 KRISHI SAARTHI</h1>
    <p><b>Your Farm. Your Future.</b></p>
    <p>Your Trusted Partner in Smart Farming</p>
</div>
""", unsafe_allow_html=True)


# ---------------- TOP NAVIGATION ----------------

st.markdown('<div class="nav-label">QUICK NAVIGATION</div>',
            unsafe_allow_html=True)

nav_items = [
    ("🏠 Dashboard", None),
    ("🤖 Kisan AI", "pages/1_Kisan_AI.py"),
    ("🌦️ Weather", "pages/3_Weather_Forecast.py"),
    ("🌾 Crops", "pages/2_Crop_Recommendation.py"),
    ("📈 Mandi Rates", "pages/8_Mandi_Rates.py"),
    ("🏛️ Schemes", "pages/10_Government_Schemes.py")
]

nav_cols = st.columns(6)

for col, (label, page) in zip(nav_cols, nav_items):
    with col:
        if page:
            st.page_link(page, label=label)
        else:
            st.page_link("main.py", label=label)


# ---------------- SERVICES SECTION ----------------

st.markdown("")
st.markdown(
    '<div class="nav-label">YOUR DIGITAL FARMING TOOLKIT</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='margin-top:0;margin-bottom:5px;'>"
    "Explore All Services 🌿</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#718071;font-size:13px;margin-bottom:15px;'>"
    "Choose any service to get started. All your farming tools are here."
    "</p>",
    unsafe_allow_html=True
)


# ---------------- SERVICE GRID ----------------

# Five columns on wide screens; cards remain compact.
for start in range(0, len(modules), 5):
    cols = st.columns(5)

    for col, module in zip(cols, modules[start:start + 5]):
        icon, name, description, page = module

        with col:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-icon">{icon}</div>
                <div class="service-name">{name}</div>
                <div class="service-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)

            st.page_link(
                page,
                label="Open →"
            )


# ---------------- SMALL FOOTER ----------------

st.markdown("""
<div class="footer">
    <b>🌱 KRISHI SAARTHI</b><br>
    Your Trusted Partner in Smart Farming |
    Empowering Farmers Through Technology
</div>
""", unsafe_allow_html=True)
