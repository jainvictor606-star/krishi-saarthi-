
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Greenhouse Management | Krishi Saarthi",
    page_icon="🏡",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"


# Gemini greenhouse assistant
def get_greenhouse_plan(details, language):

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=30000)
    )

    prompt = f"""
    You are KRISHI SAARTHI Greenhouse Planning Assistant.

    Prepare a practical greenhouse planning guide using:
    {details}

    Reply in {language}.

    Include:
    1. Suitable greenhouse type and why.
    2. Suggested structure and covering materials.
    3. Ventilation and temperature management.
    4. Irrigation and water management.
    5. Suitable crops to consider.
    6. Basic maintenance requirements.
    7. Important setup precautions.
    8. Questions the farmer should ask a local supplier.

    Important:
    - Do not guarantee crop yield or profit.
    - Do not invent market prices or subsidy amounts.
    - Clearly distinguish estimates from verified facts.
    - Recommend consulting local agricultural experts.
    - Government subsidy eligibility and availability must
      be verified with the relevant state horticulture department.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            temperature=0.4
        )
    )

    return response.text


st.title("🏡 Greenhouse Management")
st.caption("Plan, estimate and manage your greenhouse.")

st.divider()

language = st.selectbox(
    "Select Language",
    ["English", "Hindi", "Punjabi"]
)

plan_tab, cost_tab, scheme_tab = st.tabs(
    [
        "🌱 Greenhouse Planner",
        "💰 Cost Calculator",
        "🏛️ Government Schemes"
    ]
)


# TAB 1: GREENHOUSE PLANNER
with plan_tab:

    st.subheader("🌿 Plan Your Greenhouse")

    with st.form("greenhouse_form"):

        col1, col2 = st.columns(2)

        with col1:

            location = st.text_input(
                "Village / District / State",
                placeholder="Example: Phagwara, Punjab"
            )

            area = st.number_input(
                "Available Land Area (Square Metres)",
                min_value=10.0,
                max_value=100000.0,
                value=500.0
            )

            greenhouse_type = st.selectbox(
                "Greenhouse Type",
                [
                    "Naturally Ventilated Greenhouse",
                    "Fan and Pad Greenhouse",
                    "Shade Net House",
                    "Polyhouse",
                    "Not Sure - Recommend One"
                ]
            )

        with col2:

            crop = st.selectbox(
                "Crop You Want to Grow",
                [
                    "Tomato",
                    "Capsicum",
                    "Cucumber",
                    "Strawberry",
                    "Flowers",
                    "Leafy Vegetables",
                    "Other / Not Decided"
                ]
            )

            budget = st.selectbox(
                "Approximate Budget",
                [
                    "Below ₹1 Lakh",
                    "₹1–5 Lakh",
                    "₹5–10 Lakh",
                    "₹10–25 Lakh",
                    "Above ₹25 Lakh",
                    "Not Decided"
                ]
            )

            water = st.selectbox(
                "Water Availability",
                ["High", "Moderate", "Limited"]
            )

        extra = st.text_area(
            "Additional Requirements",
            placeholder="Example: I want drip irrigation and natural ventilation."
        )

        submitted = st.form_submit_button(
            "🌱 Generate Greenhouse Plan",
            use_container_width=True
        )

    if submitted:

        if not location.strip():
            st.warning("Please enter your location.")

        else:

            details = {
                "Location": location,
                "Area": f"{area} square metres",
                "Greenhouse Type": greenhouse_type,
                "Crop": crop,
                "Budget": budget,
                "Water Availability": water,
                "Additional Requirements": extra
            }

            with st.spinner("Preparing your greenhouse plan..."):

                try:
                    result = get_greenhouse_plan(
                        details,
                        language
                    )

                    st.success("Greenhouse plan generated!")
                    st.subheader("Your Greenhouse Plan")
                    st.markdown(result)

                except Exception as e:
                    st.error("Unable to generate the plan.")
                    st.caption(f"Error: {e}")


# TAB 2: COST CALCULATOR
with cost_tab:

    st.subheader("💰 Greenhouse Setup Cost Calculator")

    st.info(
        "Enter estimated local supplier rates. "
        "The calculator uses your inputs, not live market prices."
    )

    area_cost = st.number_input(
        "Greenhouse Area (Square Metres)",
        min_value=10.0,
        value=500.0,
        step=10.0
    )

    structure_rate = st.number_input(
        "Structure Cost per Square Metre (₹)",
        min_value=0,
        value=500,
        step=50
    )

    covering_rate = st.number_input(
        "Covering Material Cost per Square Metre (₹)",
        min_value=0,
        value=150,
        step=10
    )

    irrigation_rate = st.number_input(
        "Irrigation System Total Cost (₹)",
        min_value=0,
        value=25000,
        step=1000
    )

    ventilation_cost = st.number_input(
        "Ventilation / Cooling Total Cost (₹)",
        min_value=0,
        value=20000,
        step=1000
    )

    labour_cost = st.number_input(
        "Installation and Labour Cost (₹)",
        min_value=0,
        value=30000,
        step=1000
    )

    other_cost = st.number_input(
        "Other Expenses (₹)",
        min_value=0,
        value=10000,
        step=1000
    )

    contingency_percent = st.slider(
        "Extra Contingency (%)",
        min_value=0,
        max_value=20,
        value=10
    )

    if st.button(
        "Calculate Estimated Cost",
        use_container_width=True
    ):

        structure_total = area_cost * structure_rate
        covering_total = area_cost * covering_rate

        subtotal = (
            structure_total
            + covering_total
            + irrigation_rate
            + ventilation_cost
            + labour_cost
            + other_cost
        )

        contingency = subtotal * contingency_percent / 100

        total = subtotal + contingency

        st.divider()
        st.subheader("📊 Estimated Budget")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Base Cost",
            f"₹{subtotal:,.0f}"
        )

        col2.metric(
            "Contingency",
            f"₹{contingency:,.0f}"
        )

        col3.metric(
            "Total Estimated Cost",
            f"₹{total:,.0f}"
        )

        breakdown = {
            "Structure": structure_total,
            "Covering Material": covering_total,
            "Irrigation": irrigation_rate,
            "Ventilation / Cooling": ventilation_cost,
            "Labour": labour_cost,
            "Other Expenses": other_cost,
            "Contingency": contingency
        }

        st.bar_chart(breakdown)

        st.caption(
            "This is a preliminary estimate only. "
            "Actual costs depend on design, specifications, "
            "supplier quotations, transport and local conditions."
        )


# TAB 3: GOVERNMENT SCHEMES
with scheme_tab:

    st.subheader("🏛️ Greenhouse Government Support")

    st.write(
        "Farmers may be eligible for assistance under "
        "horticulture development programmes, depending "
        "on current scheme guidelines."
    )

    st.markdown("""
    **Where to check:**

    1. MIDH – Mission for Integrated Development of Horticulture.
    2. State Horticulture Department.
    3. District Horticulture Officer.
    4. Local Krishi Vigyan Kendra (KVK).

    **Before applying, verify:**

    - Current application window.
    - Eligible greenhouse structures.
    - Farmer category and land requirements.
    - Approved cost norms and subsidy limits.
    - Required documents and inspection process.
    """)

    st.warning(
        "Subsidy is not guaranteed. Rates, eligibility and "
        "application procedures can change. Confirm current "
        "details with the official department before investing."
    )

    st.link_button(
        "Visit MIDH Official Website",
        "https://midh.gov.in/"
    )

st.divider()
st.caption("KRISHI SAARTHI | Greenhouse Intelligence")
