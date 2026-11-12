
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Soil Health Analysis | Krishi Saarthi",
    page_icon="🌍",
    layout="wide"
)

MODEL_NAME = "gemini-3.5-flash"


def analyze_soil(details, language):

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=30000)
    )

    prompt = f"""
    You are KRISHI SAARTHI Soil Health Assistant.

    Analyze the following soil test information:
    {details}

    Reply in {language}.

    Prepare a report with:
    1. Soil pH interpretation.
    2. Nitrogen, phosphorus and potassium observations.
    3. Organic carbon interpretation.
    4. Possible soil fertility limitations.
    5. General soil improvement practices.
    6. Crop suitability considerations.
    7. What the farmer should discuss with a soil expert.

    Important:
    - NPK values are provided in kg/ha.
    - Organic carbon is provided as percentage.
    - Do not invent missing values.
    - Do not assume universal NPK thresholds.
    - Interpret values cautiously because soil type,
      testing method and regional standards matter.
    - Never prescribe exact fertilizer doses.
    - Recommend a government-recognized soil testing
      laboratory for confirmation.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1500,
            temperature=0.3
        )
    )

    return response.text


st.title("🌍 Soil Health Analysis")
st.caption("Understand your soil and make informed farming decisions.")

st.divider()

language = st.selectbox(
    "Select Report Language",
    ["English", "Hindi", "Punjabi"]
)

st.subheader("🧪 Enter Your Soil Test Values")

st.info(
    "Enter values from your soil testing report. "
    "For this prototype, NPK must be entered in kg/ha "
    "and Organic Carbon in percentage."
)

with st.form("soil_health_form"):

    col1, col2 = st.columns(2)

    with col1:

        location = st.text_input(
            "Farm Location",
            placeholder="Example: Phagwara, Punjab"
        )

        soil_type = st.selectbox(
            "Soil Type",
            [
                "Alluvial Soil",
                "Sandy Soil",
                "Clay Soil",
                "Loamy Soil",
                "Black Soil",
                "Red Soil",
                "Unknown"
            ]
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=7.0,
            step=0.1
        )

        organic_carbon = st.number_input(
            "Organic Carbon (%)",
            min_value=0.0,
            max_value=20.0,
            value=0.5,
            step=0.1
        )

    with col2:

        nitrogen = st.number_input(
            "Available Nitrogen (kg/ha)",
            min_value=0.0,
            value=280.0,
            step=10.0
        )

        phosphorus = st.number_input(
            "Available Phosphorus (kg/ha)",
            min_value=0.0,
            value=20.0,
            step=1.0
        )

        potassium = st.number_input(
            "Available Potassium (kg/ha)",
            min_value=0.0,
            value=180.0,
            step=10.0
        )

        previous_crop = st.text_input(
            "Previously Grown Crop",
            placeholder="Example: Wheat"
        )

    additional_info = st.text_area(
        "Additional Information (Optional)",
        placeholder="Enter any other observations from your soil report..."
    )

    submitted = st.form_submit_button(
        "🔬 Analyze Soil Health",
        use_container_width=True
    )


if submitted:

    if not location.strip():
        st.warning("Please enter your farm location.")

    else:

        details = {
            "Location": location,
            "Soil Type": soil_type,
            "pH": ph,
            "Organic Carbon": f"{organic_carbon}%",
            "Nitrogen": f"{nitrogen} kg/ha",
            "Phosphorus": f"{phosphorus} kg/ha",
            "Potassium": f"{potassium} kg/ha",
            "Previous Crop": previous_crop or "Not provided",
            "Additional Information": additional_info or "None"
        }

        with st.spinner("Gemini AI is analyzing your soil..."):

            try:

                result = analyze_soil(
                    details,
                    language
                )

                st.success("Soil analysis completed!")

                st.divider()

                st.subheader("🌱 Your Soil Health Report")
                st.markdown(result)

                st.info(
                    "This is an AI-assisted interpretation, not "
                    "a certified laboratory report. Confirm "
                    "fertility and fertilizer decisions with "
                    "a qualified soil expert."
                )

            except Exception as e:

                st.error("Unable to analyze soil information.")

                st.caption(f"Error: {e}")


st.divider()
st.caption("KRISHI SAARTHI | Powered by Gemini AI")
